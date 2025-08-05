from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# endpoint -> membuka halaman utama
@app.get('/')
def getMain():
    return {
        "message" : "welcome!"
    }

# jalankan dengan : fastapi dev main.py

#endpoint 2 -> menampilkan data dari csv
@app.get("/detail")
def getDetail():
    df = pd.read_csv('data.csv')

    return{
        "message" : "This is detail page",
        "dataDict" : df.to_dict(),
        "dataRecords" : df.to_dict(orient='records')
    } 

# endpoint 3 -> menampilkan data spesific sesuai dengan filter
# path-parameter -> sebuah input yang bisa dimasukkan kedalam URL
@app.get("/detail/{id}")
def getDataById(id: int):
    df = pd.read_csv('data.csv')
    # filter
    result = df.query(f"id == {id}")

    #cek apakah hasil filter ada isinya
    # ada -> success, ga ada eror
    if result.empty :
        raise HTTPException(status_code = 404, detail="data tidak ditemukan" )

    return {
        "data": result.to_dict(orient="records")
    }

# endpoint 4
@app.deletes(f"/getDetail/{id}")
def deleteDataById(id: int):
    df = pd.read_csv ('data.csv')

    result = df.query(f"id == {id}")

    # cek apakah hasil filter ada isinya
    # ada -> success, gaada -> error
    if result.empty:
        # kasih error
        raise HTTPException(status_code = 404, detail="data tidak ditemukan" )
    
    #delete
    df = df.query(f"id != {id}")
    df.to_csv('data.csv', index=False)

    return {
        "message": "data berhasil dihapus!"
    }