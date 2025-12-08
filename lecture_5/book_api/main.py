# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Import local modules
import models
import schemas
from database import engine, SessionLocal

# Create database tables automatically based on models
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple Book Collection API")

# Dependency: Get DB Session
def get_db():
    """
    Creates a new database session for a request and closes it afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. POST /books/ - Add a new book
@app.post("/books/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book in the database.
    """
    # Create ORM model instance
    new_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book) # Refresh to get the generated ID
    return new_book

# 2. GET /books/ - Get all books
@app.get("/books/", response_model=List[schemas.BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of books with optional pagination.
    """
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

# 5. GET /books/search/ - Search books
# Placed before /{book_id} to avoid route conflict
@app.get("/books/search/", response_model=List[schemas.BookResponse])
def search_books(
    title: Optional[str] = Query(None, min_length=1),
    author: Optional[str] = Query(None, min_length=1),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Search books by title, author, or year.
    Returns books that match ANY of the provided criteria (OR logic),
    or ALL criteria (AND logic). Let's implement flexible filtering (AND logic).
    """
    query = db.query(models.Book)
    
    if title:
        # Case-insensitive search using ilike (standard SQL) or python logic
        query = query.filter(models.Book.title.contains(title))
    if author:
        query = query.filter(models.Book.author.contains(author))
    if year:
        query = query.filter(models.Book.year == year)
        
    results = query.all()
    
    if not results:
        # Depending on requirements, return empty list or 404.
        # Returning empty list is standard for search.
        return []
        
    return results

# 4. PUT /books/{book_id} - Update book details
@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book_update: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Update an existing book by ID.
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Update fields
    db_book.title = book_update.title
    db_book.author = book_update.author
    db_book.year = book_update.year
    
    db.commit()
    db.refresh(db_book)
    return db_book

# 3. DELETE /books/{book_id} - Delete a book by ID
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by ID. Returns 204 No Content on success.
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return None