# Ecommerce-system
Este proyecto es un rest-api creado en fastapi. 
Es un sistema pensado para un ecommerce. 
Esta montado en docker-compose y despliega un servidor fastapi, una base de datos postgresql, y una base de datos mongodb.

Mas adelante se daran detalles de las funcionalidades que presenta.

## Primeros Pasos

1. Descargar el repositorio a una carpeta local
2. ***IMPORTANTE*** Crear una carpeta llamada versions/ en la ruta app/alembic/ es importante que la carpeta este creada y vacia antes de realizar el siguiente paso
3. Si no se tiene instalado docker instalar docker compose. 
  https://docs.docker.com/desktop/install/linux-install/
4. En la carpeta de origen del repositorio ejecutar el comando: `docker-compose up`
5. Entrar a la url http://0.0.0.0:8000/docs dentro de su navegador para visualizar la documentación de fastapi.
6. Ejecutar la ruta /api/v1/create/data/db/ en la seccion "db". Esto creara los siguientes usuarios y productos, permitiendo usar el sistema.

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


## Estructura de la base de datos

![Modelo entidad relacion!](/base_de_datos.png "Modelo entidad relacion")


## Funcionalidades

Para las funcionalidades solicitadas, se enlistara a continuación cada uno de los requerimientos con sus respectivas rutas que los cumplen. 

De manera general se cumplen los siguientes requerimientos:
1. El sistema cuenta con los roles (Anonymous, Seller, Admin Platform..., Admin, Financial, Logistics)
2. Cuenta con un login para poder iniciar sesión
3. Solo los Sellers y Buyers se pueden registrar, se verifica que el correo no este registrado ya y que no este en blacklist por medio de un servicio externo. 
4. Cualquier usuario registrado puede iniciar sesion con su correo y contraseña
5. Se guarda la contraseña cifrada por seguridad
6. Se integro JWT al sistema como autenticación
7. En cada petición se verifica que el usuario tenga los permisos para esa peticion por medio del JWT
8. Se utilizo una base de datos Postgresql
9. Se creo el test solicitado.

### Requerimientos del admin
Los requerimientos del admin en cuanto al manejo de usuarios se  encuentran en la sección de Admin dentro de la documentación. Necesitan autenticación como admin para poderse ejecutar.


### Requerimientos del Seller
Los requerimientos de seller se encuentran en la sección de Seller dentro de la documentación. Necesitan autenticación como seller y quien las ejecute sea dueño del producto 

### Lista de productos y filtros
Accesibles para cualquier usuario. Sin necesidad de estar logeado. Se encuentran en la sección de Products.

### Requerimientos de Logistics
Los requerimientos de logistics se encuentran en la sección de Logistics dentro de la documentación. Necesitan autenticación como logistict para ser ejecutadas.

### Log para productos y ordenes
Se encuentran en la sección de admin. 

### Requerimientos de financial
Los requerimientos de financial se encuentran en la sección de Finantial dentro de la documentación. Necesitan autenticación como Finantial para ser ejecutadas.

### Para crear una orden asociada a varios productos
Se encuentra en la sección de logistics con la ruta `/api/v1/logistics/orders/` y metodo `Post`




