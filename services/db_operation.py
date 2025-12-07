import pandas as pd
import numpy as np

FRONT_FILE_PATH = "data/front_analytics_sample.xlsx"
SNOWFLAKE_FILE_PATH = "data/messages_table_sample.xlsx"


def _df_to_safe_records(df: pd.DataFrame):
    # Replace infinite values and NaN with None so JSON serialization succeeds
    df = df.replace([np.inf, -np.inf], None)
    df = df.replace([np.nan], None)

    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")


def load_overall_usage():
    df = pd.read_excel(FRONT_FILE_PATH, sheet_name="overall_usage")
    return _df_to_safe_records(df)


def load_user_usage():
    df = pd.read_excel(FRONT_FILE_PATH, sheet_name="user_usage")
    return _df_to_safe_records(df)


def load_messages():
    df = pd.read_excel(SNOWFLAKE_FILE_PATH, sheet_name="messages")
    columns = ['message_id',
            'conversation_id',
            'user_id',
            'sender_name',
            'sender_email',
            'timestamp',
            'direction',
            'body',
            'sentiment',
            'score',
            'emotion',
            'tone',
            'analyzed'
            ]
    df = df[columns]
    return _df_to_safe_records(df)


async def save_message(message: dict):
    """Save or update a single message entry in the Snowflake file.
    
    Args:
        message: Dictionary containing message data with 'message_id' key
    """
    try:
        df = pd.read_excel(SNOWFLAKE_FILE_PATH, sheet_name="messages")
        
        message_id = message.get('message_id')
        if not message_id:
            raise ValueError("Message must have 'message_id' field")
        
        # Convert message_id to string for comparison
        message_id_str = str(message_id)
        
        # Check if message exists
        if message_id_str in df['message_id'].astype(str).values:
            # Update existing message - update row by row
            for col in message.keys():
                if col in df.columns:
                    df.loc[df['message_id'].astype(str) == message_id_str, col] = message[col]
        else:
            # Add new message as a new row
            new_row = pd.DataFrame([message])
            df = pd.concat([df, new_row], ignore_index=True)
        
        # Write back to Excel
        with pd.ExcelWriter(SNOWFLAKE_FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='messages', index=False)
    except Exception as e:
        raise Exception(f"Error saving message: {str(e)}")

