from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, oauth2, schemas
from ..database import get_db
from passlib.context import CryptContext
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)


@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user),
                  limit: int = 10, skip: int = 0, search: Optional[str]=""):
                  
     #only returns published posts: .filter(models.Post.published==True)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    #cur.execute("""SELECT * FROM posts""")
    #posts = cur.fetchall()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
     #           (post.title, post.content, post.published))
    #new_post = cur.fetchone()
    #conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
   # cur.execute("SELECT * FROM posts WHERE id = %s ", (str(id),))
    #post = cur.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    deletion_post = deleted_post.first()
    #cur.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cur.fetchone()
    #conn.commit()
    if deletion_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    if deletion_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not Authorized to perform action")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model = schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""",
    #             (post.title, post.content, post.published, (str(id))))
    #updated_post = cur.fetchone()
    #conn.commit()
    updated_postquery = db.query(models.Post).filter(models.Post.id == id)
    post = updated_postquery.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not Authorized to perform action")
    updated_postquery.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return updated_postquery.first()

