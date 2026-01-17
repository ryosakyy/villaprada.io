from sqlalchemy.orm import Session
from models.galeria import Galeria
from schemas.galeria import GaleriaCreate, GaleriaUpdate
import cloudinary.uploader

class GaleriaService:

    # Crear simple
    @staticmethod
    def crear_galeria(db: Session, data: GaleriaCreate, imagen_url: str, public_id: str):
        nueva = Galeria(
            titulo=data.titulo,
            descripcion=data.descripcion,
            categoria=data.categoria,
            contrato_id=data.contrato_id,
            imagen_url=imagen_url,
            public_id=public_id,
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def listar_galeria(db: Session):
        return db.query(Galeria).order_by(Galeria.fecha_creacion.desc()).all()

    @staticmethod
    def obtener_galeria(id: int, db: Session):
        return db.query(Galeria).filter(Galeria.id == id).first()

    @staticmethod
    def listar_por_categoria(categoria: str, db: Session):
        return db.query(Galeria).filter(
            Galeria.categoria.ilike(f"%{categoria}%")
        ).order_by(Galeria.fecha_creacion.desc()).all()

    @staticmethod
    def actualizar_galeria(id: int, data: GaleriaUpdate, db: Session):
        gal = db.query(Galeria).filter(Galeria.id == id).first()
        if not gal:
            return None

        for campo, valor in data.dict(exclude_unset=True).items():
            setattr(gal, campo, valor)

        db.commit()
        db.refresh(gal)
        return gal

    @staticmethod
    def eliminar_galeria(id: int, db: Session):
        gal = db.query(Galeria).filter(Galeria.id == id).first()
        if not gal:
            return None

        db.delete(gal)
        db.commit()
        return True

    # ================= Subida múltiple ======================
    @staticmethod
    def crear_galeria_masiva(db, archivos, categoria, contrato_id):
        resultados = []

        for i, archivo in enumerate(archivos):
            result = cloudinary.uploader.upload(
                archivo.file,
                folder="villa_prada/galeria",
                resource_type="image",
            )

            nueva = Galeria(
                titulo=f"Imagen {i+1}",
                descripcion=None,
                categoria=categoria,
                contrato_id=contrato_id,
                imagen_url=result.get("secure_url"),
                public_id=result.get("public_id"),
            )

            db.add(nueva)
            db.commit()
            db.refresh(nueva)

            resultados.append(nueva)

        return resultados

    # ================== PAGINADO ============================
    @staticmethod
    def paginado(db, page: int, limit: int):
        offset = (page - 1) * limit
        return db.query(Galeria).order_by(
            Galeria.fecha_creacion.desc()
        ).offset(offset).limit(limit).all()

    # ================= BUSQUEDA ============================
    @staticmethod
    def buscar(db, texto: str):
        texto = f"%{texto.lower()}%"
        return db.query(Galeria).filter(
            (Galeria.titulo.ilike(texto)) |
            (Galeria.descripcion.ilike(texto)) |
            (Galeria.categoria.ilike(texto))
        ).all()

    # ================= LIGHT ================================
    @staticmethod
    def galeria_light(db):
        items = db.query(Galeria).order_by(Galeria.fecha_creacion.desc()).all()
        return [
            {
                "id": g.id,
                "titulo": g.titulo,
                "imagen": g.imagen_url, # Legacy
                "imagen_url": g.imagen_url, # Standard (Consistency)
                "secure_url": g.imagen_url, # Extra safety
                "categoria": g.categoria,
            }
            for g in items
        ]
