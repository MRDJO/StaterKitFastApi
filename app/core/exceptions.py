from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

class CustomException(HTTPException):
   def __init__(self,status_code: int, detail : str):
      super().__init__(status_code= status_code, detail=detail)

def not_found_exception(detail: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

def not_authorize_exception(detail: str):
    raise HTTPException(status_code=401, detail=detail)


def integrityError(detail: str):
   raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def serverInterneError(detail: str):
   raise HTTPException(status_code=500, detail=detail)


def bad_request_object(detail: str):
   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)



