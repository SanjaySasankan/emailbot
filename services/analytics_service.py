from .db_operation import load_overall_usage, load_user_usage
from collections import defaultdict
from services.message_service import get_message_summary
import pandas as pd

def get_team_summary():
    data = load_overall_usage()
    return {row["Metric"]: row["Value"] for row in data}

def get_users_summary():
    return load_user_usage()

def get_user_report(user_id: str):
    users = load_user_usage()
    for u in users:
        if u["User ID"] == user_id:
            return u
    return None

def aggregate_user_sentiment():

    df_users = pd.DataFrame(get_users_summary())
    df_messages = pd.DataFrame(get_message_summary())

    # -------------------------------------
    # 1. FILTER FOR OUTBOUND MESSAGES FIRST
    # -------------------------------------
    df_agents = df_messages[df_messages["direction"] == "outbound"].copy()

    # -------------------------------------
    # 2. MERGE USERS → MESSAGES (your request)
    # -------------------------------------
    df_merged = df_users.merge(
        df_agents,
        how="left",
        left_on="User Email",      # user-level primary key
        right_on="sender_email"    # message-level sender
    )

    # -------------------------------------
    # 3. SENTIMENT COUNTS PER USER
    # -------------------------------------
    sentiment_counts = (
        df_merged
        .pivot_table(
            index="User Email",
            columns="sentiment",
            aggfunc="size",
            fill_value=0
        )
        .reset_index()
        .rename(columns={
            "positive": "positive_count",
            "negative": "negative_count",
            "neutral": "neutral_count"
        })
    )

    # -------------------------------------
    # 4. AVERAGE SENTIMENT SCORE
    # -------------------------------------
    avg_scores = (
        df_merged
        .groupby("User Email")["score"]
        .mean()
        .reset_index(name="avg_score")
    )

    # -------------------------------------
    # 5. TOP EMOTION
    # -------------------------------------
    top_emotion = (
        df_merged
        .groupby("User Email")["emotion"]
        .agg(lambda s: s.mode().iat[0] if not s.mode().empty else None)
        .reset_index(name="top_emotion")
    )

    # -------------------------------------
    # 6. TOP TONE
    # -------------------------------------
    top_tone = (
        df_merged
        .groupby("User Email")["tone"]
        .agg(lambda s: s.mode().iat[0] if not s.mode().empty else None)
        .reset_index(name="top_tone")
    )

    # -------------------------------------
    # 7. MESSAGE COUNT
    # -------------------------------------
    msg_counts = (
        df_merged
        .groupby("User Email")
        .size()
        .reset_index(name="message_count")
    )

    # -------------------------------------
    # 8. FINAL MERGE → USERS AS PRIMARY TABLE
    # -------------------------------------
    df_final = (
        df_users
        .merge(sentiment_counts, on="User Email", how="left")
        .merge(avg_scores, on="User Email", how="left")
        .merge(top_emotion, on="User Email", how="left")
        .merge(top_tone, on="User Email", how="left")
        .merge(msg_counts, on="User Email", how="left")
    )

    # -------------------------------------
    # 9. FILL EMPTY VALUES (do it column-by-column to avoid pandas validation issues)
    # -------------------------------------
    defaults = {
        "positive_count": 0,
        "negative_count": 0,
        "neutral_count": 0,
        "avg_score": 0,
        "top_emotion": None,
        "top_tone": None,
        "message_count": 0,
    }

    # for col, val in defaults.items():
    #     if col in df_final.columns:
    #         df_final[col] = df_final[col].fillna(val)

    # -------------------------------------
    # 10. ATTACH OUTBOUND MESSAGES PER USER
    # -------------------------------------
    msg_cols = [
        "message_id", "conversation_id", "sender_email",
        "timestamp", "direction", "body",
        "sentiment", "score", "emotion", "tone", "analyzed"
    ]

    present_cols = [c for c in msg_cols if c in df_merged.columns]

    messages_grouped = (
        df_merged
        .groupby("User Email")[present_cols]
        .apply(lambda g: g.to_dict(orient="records"))
        .reset_index(name="messages")
    )

    df_final = df_final.merge(messages_grouped, on="User Email", how="left")
    df_final["messages"] = df_final["messages"].apply(
        lambda x: x if isinstance(x, list) else []
    )

    return df_final
