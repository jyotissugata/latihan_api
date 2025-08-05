from fastapi import FastAPI, HTTPException, Header
import pandas as pd

app = FastAPI()
password = 'secret123'

# endpoint -> membuka halaman utama
@app.get('/')
def getMain():
    return {
        "message" : "welcome!"
    }

# jalankan dengan : fastapi dev main.py
# stop dengan ctrl + c

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

    # cek apakah hasil filter ada isinya
    # ada -> success, gaada -> error
    if result.empty:
        # kasih error
        raise HTTPException(status_code=404, detail="data tidak ditemukan!")

    return {
        "data": result.to_dict(orient="records")
    }

# endpoint 4 -> delete data by id
# apply auth
@app.delete("/detail/{id}")
def deleteDataById(id: int, api_key: str = Header()):
    # check api_key
    # benar -> lanjut, salah -> error
    if api_key == None or api_key != password:
        # kasih error
        raise HTTPException(status_code=401, detail="password salah!")

    df = pd.read_csv('data.csv')

    # filter
    result = df.query(f"id == {id}")

    # cek apakah hasil filter ada isinya
    # ada -> lanjut ke delete, gaada -> error
    if result.empty:
        # kasih error
        raise HTTPException(status_code=404, detail="data tidak ditemukan!")
    
    # delete -> exclude id yang ada di parameter
    df = df.query(f"id != {id}")

    # update dataset -> replace dataset yang lama dengan yang baru
    df.to_csv('data.csv', index=False)

    return {
        "message": "data berhasil dihapus!"
    }