from typing import Optional
import datetime
import decimal
import uuid

from sqlalchemy import Boolean, CheckConstraint, DateTime, Enum, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class CategoriaContabilidad(Base):
    __tablename__ = 'categoria_contabilidad'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='categoria_contabilidad_pkey'),
        UniqueConstraint('codigo', name='categoria_contabilidad_codigo_key'),
        UniqueConstraint('nombre', name='categoria_contabilidad_nombre_key'),
        Index('ix_categoria_contabilidad_id', 'id')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)

    cartera: Mapped[list['Cartera']] = relationship('Cartera', back_populates='categoria_contabilidad')
    ingreso: Mapped[list['Ingreso']] = relationship('Ingreso', back_populates='categoria_contabilidad')


class RefMovimiento(Base):
    __tablename__ = 'ref_movimiento'
    __table_args__ = (
        PrimaryKeyConstraint('ref_movimiento_id', name='ref_movimiento_pkey'),
        UniqueConstraint('nombre', name='ref_movimiento_nombre_key'),
        Index('ix_ref_movimiento_ref_movimiento_id', 'ref_movimiento_id')
    )

    ref_movimiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))

    movimientos_stock: Mapped[list['MovimientosStock']] = relationship('MovimientosStock', back_populates='ref_movimiento')


class TipoMovimiento(Base):
    __tablename__ = 'tipo_movimiento'
    __table_args__ = (
        PrimaryKeyConstraint('tipo_movimiento_id', name='tipo_movimiento_pkey'),
        UniqueConstraint('nombre', name='tipo_movimiento_nombre_key'),
        Index('ix_tipo_movimiento_tipo_movimiento_id', 'tipo_movimiento_id')
    )

    tipo_movimiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))

    movimientos_stock: Mapped[list['MovimientosStock']] = relationship('MovimientosStock', back_populates='tipo_movimiento')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='user_pkey'),
        Index('ix_user_correo', 'correo', unique=True),
        Index('ix_user_full_name', 'nombre_completo'),
        Index('ix_user_user_id', 'user_id')
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    correo: Mapped[str] = mapped_column(String(255), nullable=False)
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(Enum('administrador', 'vendedor', name='user_role'), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    creado_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    actualizado_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    nombre_completo: Mapped[Optional[str]] = mapped_column(String(150))
    numero_contacto: Mapped[Optional[str]] = mapped_column(String(50))

    categoria: Mapped[list['Categoria']] = relationship('Categoria', foreign_keys='[Categoria.actualizado_por_id]', back_populates='actualizado_por')
    categoria_: Mapped[list['Categoria']] = relationship('Categoria', foreign_keys='[Categoria.creado_por_id]', back_populates='creado_por')
    product: Mapped[list['Product']] = relationship('Product', foreign_keys='[Product.actualizado_por_id]', back_populates='actualizado_por')
    product_: Mapped[list['Product']] = relationship('Product', foreign_keys='[Product.creado_por_id]', back_populates='creado_por')
    stock: Mapped[list['Stock']] = relationship('Stock', foreign_keys='[Stock.actualizado_por_id]', back_populates='actualizado_por')
    stock_: Mapped[list['Stock']] = relationship('Stock', foreign_keys='[Stock.creado_por_id]', back_populates='creado_por')
    movimientos_stock: Mapped[list['MovimientosStock']] = relationship('MovimientosStock', back_populates='realizado_por')
    ventas: Mapped[list['Venta']] = relationship('Venta', back_populates='usuario')


class Cliente(Base):
    __tablename__ = 'clientes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='clientes_pkey'),
        Index('ix_clientes_id', 'id'),
        Index('ix_clientes_nombre_normalizado', 'nombre_normalizado')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre_normalizado: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, default=datetime.datetime.utcnow)


class Cartera(Base):
    __tablename__ = 'cartera'
    __table_args__ = (
        CheckConstraint('monto >= 0::numeric', name='ck_cartera_monto_no_negativo'),
        ForeignKeyConstraint(['categoria_contabilidad_id'], ['categoria_contabilidad.id'], ondelete='SET NULL', name='cartera_categoria_contabilidad_id_fkey'),
        PrimaryKeyConstraint('cartera_id', name='cartera_pkey'),
        Index('ix_cartera_cartera_id', 'cartera_id'),
        Index('ix_cartera_fecha', 'fecha')
    )

    cartera_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    monto: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    categoria_contabilidad_id: Mapped[Optional[int]] = mapped_column(Integer)
    cliente: Mapped[Optional[str]] = mapped_column(String(150))
    notas: Mapped[Optional[str]] = mapped_column(String(255))

    categoria_contabilidad: Mapped[Optional['CategoriaContabilidad']] = relationship('CategoriaContabilidad', back_populates='cartera')


class Categoria(Base):
    __tablename__ = 'categoria'
    __table_args__ = (
        ForeignKeyConstraint(['actualizado_por_id'], ['user.user_id'], ondelete='SET NULL', name='categoria_actualizado_por_id_fkey'),
        ForeignKeyConstraint(['creado_por_id'], ['user.user_id'], ondelete='SET NULL', name='categoria_creado_por_id_fkey'),
        PrimaryKeyConstraint('categoria_id', name='categoria_pkey'),
        UniqueConstraint('nombre', name='categoria_nombre_key'),
        Index('ix_categoria_categoria_id', 'categoria_id')
    )

    categoria_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))
    creado_por_id: Mapped[Optional[int]] = mapped_column(Integer)
    actualizado_por_id: Mapped[Optional[int]] = mapped_column(Integer)

    actualizado_por: Mapped[Optional['User']] = relationship('User', foreign_keys=[actualizado_por_id], back_populates='categoria')
    creado_por: Mapped[Optional['User']] = relationship('User', foreign_keys=[creado_por_id], back_populates='categoria_')
    egreso: Mapped[list['Egreso']] = relationship('Egreso', back_populates='categoria')
    product: Mapped[list['Product']] = relationship('Product', back_populates='categoria')


class Ingreso(Base):
    __tablename__ = 'ingreso'
    __table_args__ = (
        CheckConstraint('monto >= 0::numeric', name='ck_ingreso_monto_no_negativo'),
        ForeignKeyConstraint(['categoria_contabilidad_id'], ['categoria_contabilidad.id'], ondelete='SET NULL', name='ingreso_categoria_contabilidad_id_fkey'),
        PrimaryKeyConstraint('ingreso_id', name='ingreso_pkey'),
        Index('ix_ingreso_fecha', 'fecha'),
        Index('ix_ingreso_ingreso_id', 'ingreso_id'),
        Index('ix_ingreso_tipo_ingreso', 'tipo_ingreso')
    )

    ingreso_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    monto: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    tipo_ingreso: Mapped[str] = mapped_column(Enum('efectivo', 'transferencia', name='tipo_ingreso_enum'), nullable=False)
    categoria_contabilidad_id: Mapped[Optional[int]] = mapped_column(Integer)
    notas: Mapped[Optional[str]] = mapped_column(String(255))
    cliente: Mapped[Optional[str]] = mapped_column(String(150))

    categoria_contabilidad: Mapped[Optional['CategoriaContabilidad']] = relationship('CategoriaContabilidad', back_populates='ingreso')


class Egreso(Base):
    __tablename__ = 'egreso'
    __table_args__ = (
        CheckConstraint('monto >= 0::numeric', name='ck_egreso_monto_no_negativo'),
        ForeignKeyConstraint(['categoria_id'], ['categoria.categoria_id'], ondelete='SET NULL', name='egreso_categoria_id_fkey'),
        PrimaryKeyConstraint('egreso_id', name='egreso_pkey'),
        Index('ix_egreso_egreso_id', 'egreso_id'),
        Index('ix_egreso_fecha', 'fecha'),
        Index('ix_egreso_tipo_egreso', 'tipo_egreso')
    )

    egreso_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    monto: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    tipo_egreso: Mapped[str] = mapped_column(Enum('efectivo', 'transferencia', name='tipo_egreso_enum'), nullable=False)
    categoria_id: Mapped[Optional[int]] = mapped_column(Integer)
    notas: Mapped[Optional[str]] = mapped_column(String(255))
    cliente: Mapped[Optional[str]] = mapped_column(String(150))

    categoria: Mapped[Optional['Categoria']] = relationship('Categoria', back_populates='egreso')


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        ForeignKeyConstraint(['actualizado_por_id'], ['user.user_id'], ondelete='SET NULL', name='product_actualizado_por_id_fkey'),
        ForeignKeyConstraint(['categoria_id'], ['categoria.categoria_id'], ondelete='SET NULL', name='product_categoria_id_fkey'),
        ForeignKeyConstraint(['creado_por_id'], ['user.user_id'], ondelete='SET NULL', name='product_creado_por_id_fkey'),
        PrimaryKeyConstraint('producto_id', name='product_pkey'),
        Index('ix_product_codigo_barras', 'codigo_barras', unique=True),
        Index('ix_product_producto_id', 'producto_id')
    )

    producto_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    codigo_barras: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    precio_venta: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    costo: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    margen: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    iva: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    categoria_id: Mapped[Optional[int]] = mapped_column(Integer)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))
    creado_por_id: Mapped[Optional[int]] = mapped_column(Integer)
    actualizado_por_id: Mapped[Optional[int]] = mapped_column(Integer)

    actualizado_por: Mapped[Optional['User']] = relationship('User', foreign_keys=[actualizado_por_id], back_populates='product')
    categoria: Mapped[Optional['Categoria']] = relationship('Categoria', back_populates='product')
    creado_por: Mapped[Optional['User']] = relationship('User', foreign_keys=[creado_por_id], back_populates='product_')
    stock: Mapped[list['Stock']] = relationship('Stock', back_populates='producto')
    movimientos_stock: Mapped[list['MovimientosStock']] = relationship('MovimientosStock', back_populates='producto')
    ventas_detalle: Mapped[list['VentaDetalle']] = relationship('VentaDetalle', back_populates='producto')


class Venta(Base):
    __tablename__ = 'venta'
    __table_args__ = (
        CheckConstraint('total >= 0::numeric', name='ck_venta_total_no_negativo'),
        ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ondelete='SET NULL', name='venta_cliente_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='SET NULL', name='venta_user_id_fkey'),
        PrimaryKeyConstraint('venta_id', name='venta_pkey'),
        Index('ix_venta_fecha', 'fecha'),
        Index('ix_venta_venta_id', 'venta_id')
    )

    venta_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    impuesto: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    descuento: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tipo_pago: Mapped[str] = mapped_column(Enum('efectivo', 'tarjeta', 'transferencia', name='tipo_pago_enum'), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    nota_venta: Mapped[Optional[str]] = mapped_column(String(255))
    cliente_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)

    cliente: Mapped[Optional['Cliente']] = relationship('Cliente')
    usuario: Mapped[Optional['User']] = relationship('User', back_populates='ventas')
    detalles: Mapped[list['VentaDetalle']] = relationship('VentaDetalle', back_populates='venta')


class VentaDetalle(Base):
    __tablename__ = 'venta_detalle'
    __table_args__ = (
        CheckConstraint('cantidad > 0', name='ck_venta_detalle_cantidad_pos'),
        ForeignKeyConstraint(['producto_id'], ['product.producto_id'], ondelete='RESTRICT', name='venta_detalle_producto_id_fkey'),
        ForeignKeyConstraint(['venta_id'], ['venta.venta_id'], ondelete='CASCADE', name='venta_detalle_venta_id_fkey'),
        PrimaryKeyConstraint('venta_detalle_id', name='venta_detalle_pkey'),
        UniqueConstraint('venta_id', 'producto_id', name='venta_detalle_venta_producto_key'),
        Index('ix_venta_detalle_venta_id', 'venta_id'),
        Index('ix_venta_detalle_producto_id', 'producto_id')
    )

    venta_detalle_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    venta_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    venta: Mapped['Venta'] = relationship('Venta', back_populates='detalles')
    producto: Mapped['Product'] = relationship('Product', back_populates='ventas_detalle')


class Stock(Base):
    __tablename__ = 'stock'
    __table_args__ = (
        ForeignKeyConstraint(['actualizado_por_id'], ['user.user_id'], ondelete='SET NULL', name='stock_actualizado_por_id_fkey'),
        ForeignKeyConstraint(['creado_por_id'], ['user.user_id'], ondelete='SET NULL', name='stock_creado_por_id_fkey'),
        ForeignKeyConstraint(['producto_id'], ['product.producto_id'], ondelete='CASCADE', name='stock_producto_id_fkey'),
        PrimaryKeyConstraint('stock_id', name='stock_pkey'),
        Index('ix_stock_stock_id', 'stock_id')
    )

    stock_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad_actual: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad_minima: Mapped[int] = mapped_column(Integer, nullable=False)
    ultima_actualizacion: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    actualizado_por_id: Mapped[Optional[int]] = mapped_column(Integer)
    creado_por_id: Mapped[Optional[int]] = mapped_column(Integer)

    actualizado_por: Mapped[Optional['User']] = relationship('User', foreign_keys=[actualizado_por_id], back_populates='stock')
    creado_por: Mapped[Optional['User']] = relationship('User', foreign_keys=[creado_por_id], back_populates='stock_')
    producto: Mapped['Product'] = relationship('Product', back_populates='stock')
    movimientos_stock: Mapped[list['MovimientosStock']] = relationship('MovimientosStock', back_populates='stock')


class MovimientosStock(Base):
    __tablename__ = 'movimientos_stock'
    __table_args__ = (
        CheckConstraint('cantidad > 0', name='ck_mov_cantidad_pos'),
        ForeignKeyConstraint(['producto_id'], ['product.producto_id'], ondelete='CASCADE', name='movimientos_stock_producto_id_fkey'),
        ForeignKeyConstraint(['realizado_por_id'], ['user.user_id'], ondelete='SET NULL', name='movimientos_stock_realizado_por_id_fkey'),
        ForeignKeyConstraint(['ref_movimiento_id'], ['ref_movimiento.ref_movimiento_id'], name='movimientos_stock_ref_movimiento_id_fkey'),
        ForeignKeyConstraint(['stock_id'], ['stock.stock_id'], ondelete='CASCADE', name='movimientos_stock_stock_id_fkey'),
        ForeignKeyConstraint(['tipo_movimiento_id'], ['tipo_movimiento.tipo_movimiento_id'], name='movimientos_stock_tipo_movimiento_id_fkey'),
        PrimaryKeyConstraint('movimiento_id', name='movimientos_stock_pkey'),
        Index('ix_movimientos_stock_movimiento_id', 'movimiento_id')
    )

    movimiento_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    stock_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_movimiento_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ref_movimiento_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    referencia_doc: Mapped[Optional[str]] = mapped_column(String(64))
    nota: Mapped[Optional[str]] = mapped_column(String(255))
    realizado_por_id: Mapped[Optional[int]] = mapped_column(Integer)

    producto: Mapped['Product'] = relationship('Product', back_populates='movimientos_stock')
    realizado_por: Mapped[Optional['User']] = relationship('User', back_populates='movimientos_stock')
    ref_movimiento: Mapped['RefMovimiento'] = relationship('RefMovimiento', back_populates='movimientos_stock')
    stock: Mapped['Stock'] = relationship('Stock', back_populates='movimientos_stock')
    tipo_movimiento: Mapped['TipoMovimiento'] = relationship('TipoMovimiento', back_populates='movimientos_stock')
