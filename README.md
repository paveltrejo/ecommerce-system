# Ecommerce-system
Este proyecto es un rest-api creado en fastapi. 
Es un sistema pensado para un ecommerce. 
Esta montado en docker-compose y despliega un servidor fastapi, una base de datos postgresql, y una base de datos mongodb.

Mas adelante se daran detalles de las funcionalidades que presenta.

## Primeros Pasos

1. Descargar el repositorio de forma local
2. Si no se tiene instalado docker instalar docker compose. 
  https://docs.docker.com/desktop/install/linux-install/
3. En la carpeta de origen del repositorio correr 'docker-compose up'
4. Entrar a la url http://0.0.0.0:8000/docs dentro de su navegador para visualizar la documentación de fastapi.
5. Ejecutar la ruta /api/v1/create/data/db/ en la seccion "db". Esto creara los siguientes usuarios y productos, permitiendo usar el sistema.

### usuarios
    buyer_user = 
        email = "buyer@gmail.com", password = "string", is_active = True  

    admin_user = 
        email = "admin@gmail.com", password = "string", is_active = True  

    finantial_user = 
        email = "finantial@gmail.com", password = "string", is_active = True  

    logistic_user = 
        email = "logistic@gmail.com", password = "string", is_active = True  

    seller_user1 = 
        email = "seller1@gmail.com", password = "string", is_active = True  

    seller_user2 = 
        email = "seller2@gmail.com", password = "string", is_active = True  


  ### productos

    new_product1 =
        name = "producto1",
        description = "descripcion de producto1",
        price = 2000,
        is_active =  True
    
    new_product2 =
        name = "producto2",
        description = "descripcion de producto2",
        price = 3000.15,
        is_active =  True
    
    new_product3 =
        name = "producto3",
        description = "descripcion de producto3",
        price = 2500,
        is_active =  True
    
    new_product4 =
        name = "producto4",
        description = "descripcion de producto4",
        price = 300.05,
        is_active =  True
    
    new_product5 =
        name = "producto5",
        description = "descripcion de producto5",
        price = 4000,
        is_active =  True
    
    new_product6 =
        name = "producto6",
        description = "descripcion de producto6",
        price = 5500.99,
        is_active =  True


## Ejecutando el test solicitado

Para ejecutar el test solo se necesita ejecutar la ruta /api/v1/test/ dentro de la sección test. Si se quiere ver el avance de cada sección se puede consultar la consola.


### Estructura de la base de datos
    

 
