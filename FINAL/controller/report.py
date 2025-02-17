from config.app import *
import pandas as pd

# crear un reporte diferente
def GenerateReportVentas(app:App):
    conn=app.bd.getConection()
    query="""
        SELECT 
            p.pais,
            v.product_id,
            SUM(v.quantity) AS total_vendido
        FROM 
            VENTAS v
        JOIN 
            POSTALCODE p
        ON 
            v.postal_code = p.code
        GROUP BY 
            p.pais, v.product_id
        ORDER BY 
            total_vendido DESC;
    """
    df=pd.read_sql_query(query,conn)
    fecha="08-02"
    path=f"D:\DATUX PYTHON\FINAL\filess-{fecha}.csv"
    df.to_csv(path)
    sendMail(app,path)


def GenerateReportClientes(app):
    conn = app.bd.get_connection() 

    query = """
        SELECT 
            c.id_cliente,
            c.nombre,
            COUNT(v.id_venta) AS total_compras,
            SUM(v.total) AS monto_total
        FROM 
            CLIENTES c
        JOIN 
            VENTAS v
        ON 
            c.id_cliente = v.id_cliente
        GROUP BY 
            c.id_cliente, c.nombre
        ORDER BY 
            monto_total DESC;
    """
    
    df = pd.read_sql_query(query, conn)
    
    fecha = "08-02"
    path = f"D:\DATUX PYTHON\FINAL\files-{fecha}.csv"
    
    df.to_csv(path, index=False)

    sendMail(app, path)

def sendMail(app:App,data):
   
    app.mail.send_email('from@example.com','Reporte_Clientes','Reporte_Clientes',data)

    