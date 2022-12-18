from fastapi import APIRouter, Depends, Response

from models.request_models import RequestBook as Request_Book
from models.request_models import ResponseBook, PutResponseBook, PutRequestBook
from models.db_models import Book as DB_Book

from db.database import get_db
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse

from exceptions.CustomHTTPException import NoContent

router = APIRouter()


@router.post('/book')
def add_new_book(
        book: Request_Book,
        data_base: Session = Depends(get_db)
):
    data_book = DB_Book(**book.dict())
    data_base.add(data_book)
    data_base.commit()
    data_base.flush()
    return JSONResponse(status_code=200, content={
        'book_id': data_book.id
    })


@router.get(
    '/book/{book_id}',
    response_model=Request_Book
)
def get_book(
        book_id: int,
        data_base: Session = Depends(get_db)
):
    data_book = data_base.query(DB_Book).get(book_id)
    if data_book is not None:
        response_book = ResponseBook(**data_book.__dict__)
        return JSONResponse(status_code=200, content={
            **response_book.dict()
        })
    else:
        raise NoContent


@router.get(
    '/books',
    response_model=list[Request_Book]
)
def get_books(
        data_base: Session = Depends(get_db)
):
    data_books = data_base.query(DB_Book).all()
    if data_books is not None:
        response_books = [ResponseBook(**x.__dict__).dict() for x in data_books]
        return JSONResponse(status_code=200, content={
            'books': response_books
        })
    else:
        raise NoContent


@router.put('/book/{book_id}')
def change_book(
        book_id,
        new_book_data: PutRequestBook,
        data_base: Session = Depends(get_db)
):
    data_book = data_base.query(DB_Book).get(book_id)
    if data_book is not None:
        data_base.query(DB_Book).\
            filter(DB_Book.id == book_id).\
            update({k: v for k, v in new_book_data.dict().items() if v is not None})
        data_base.commit()
        data_book = data_base.query(DB_Book).get(book_id)
        data_base.flush()
        response_book = PutResponseBook(**data_book.__dict__)
        return JSONResponse(status_code=200, content={
            **response_book.dict()
        })
    else:
        raise NoContent


@router.delete('/book/{book_id}')
def delete_book(
        book_id,
        data_base: Session = Depends(get_db)
):
    data_book = data_base.query(DB_Book).get(book_id)
    if data_book is not None:
        data_base.query(DB_Book).filter(DB_Book.id == book_id).delete()
        data_base.commit()
        return JSONResponse(status_code=200, content={
            'Message': 'Book has been deleted'
        })
    else:
        raise NoContent
