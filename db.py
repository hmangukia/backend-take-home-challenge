from sqlmodel import create_engine, Session

engine = create_engine(f'postgresql://hetalmangukia:postgres@localhost:5432/postgres')

def get_session():
    with Session(engine) as session:
        yield session