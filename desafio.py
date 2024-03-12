import sqlalchemy as sqA
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String(11))  # Corrigido o tamanho do CPF
    endereco = Column(String(100))  # Aumentado o tamanho do endereço

    # Definir o relacionamento entre Cliente-Conta
    conta = relationship(
        'Conta', back_populates='cliente', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})'

class Conta(Base):
    __tablename__ = "Conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    saldo = Column(Numeric(precision=10, scale=2))  # Corrigido para Numeric

    # Definindo relacionamento entre Conta-Cliente
    cliente = relationship(
        'Cliente', back_populates='conta'
    )

    def __repr__(self):
        return f'Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, id_cliente={self.id_cliente}, saldo={self.saldo})'
    

print(Cliente.__tablename__)
print(Conta.__tablename__)

engine = create_engine("sqlite://")
Base.metadata.create_all(engine)
session = Session(bind=engine)

clara = Cliente(
    nome='Clara',
    cpf='11111111111',  # Corrigido para um CPF válido
    endereco='Palitocity'
)

adriano = Cliente(
    nome='Adriano',
    cpf='22222222222',  # Corrigido para um CPF válido
    endereco='Demervascity'
)

# Adicionando contas para cada cliente
clara.conta = [
    Conta(tipo='Corrente', agencia='ABC', num=1, saldo=1000.00),
    Conta(tipo='Corrente', agencia='DEF', num=2, saldo=2000.00)
]

adriano.conta = [
    Conta(tipo='Poupança', agencia='GHI', num=3, saldo=1500.00),
    Conta(tipo='Poupança', agencia='JKL', num=4, saldo=2500.00)
]

session.add_all([clara, adriano])
session.commit()

stmt = select(Cliente).where(Cliente.nome.in_(['Clara']))
print('Recuperando usuários a partir de condição de filtragem')
for cliente in session.scalars(stmt):
    print(cliente)

stmt = select(Cliente).where(Cliente.nome.in_(['Adriano']))
print('Recuperando usuários a partir de condição de filtragem')
for cliente in session.scalars(stmt):
    print(cliente)

stmt_conta = select(Conta).where(Conta.num.in_([2]))
print('\nRecuperando o número da conta de Adriano')
for conta in session.scalars(stmt_conta):
    print(conta)

