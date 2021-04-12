import os

postgres_connection_config_params = {
    'user': os.getenv('POSTGRES_DB_USER'),
    'password': os.getenv('POSTGRES_DB_PASSWORD'),
    'host': os.getenv('POSTGRES_DB_HOST'),
    'port': os.getenv('POSTGRES_DB_PORT'),
    'database': os.getenv('POSTGRES_DB_DATABASE'),
}

integration_mode = False

target_website_simulator_url = os.getenv('TARGET_SIMULATOR_HOST')
