# Documentación de Modelos

## Modelos de `api/models.py`

### Region
- **name**: Nombre de la región.
- **creation_date**: Fecha en que se creó la región.
- **description**: Descripción de la región.
- **Relaciones**: Una región puede contener uno o varios discos.

### Disk
- **name**: Nombre del disco.
- **creation_date**: Fecha en que se creó el disco.
- **features**: Características del disco. 
  - Corresponde a un JSON donde las claves son los nombres de las características y los valores son los valores de las características. 
  - Ejemplo: `{"ID": "Oph 1", "fullname": "SSTc2dJ162623.6-242439", "RA": "16:26:23.571", "Dec": "-24:24:40.102", "SpT": "K7", "Class": "FS", "Teff": "3970", "Lstar": "0.9", "Av": "24", "Mstar": "0.6"}`. 
  - Es importante que las claves sean las mismas para todos los discos.
  - Si un disco no tiene todas las características, no es necesario incluirlas en el JSON.
- **Relaciones**: Un disco puede pertenecer a una o varias regiones y puede contener una o varias bandas.

### Band
- **name**: Nombre de la banda.
- **creation_date**: Fecha en que se creó la banda.
- **Relaciones**: Una banda puede pertenecer a uno o varios discos y puede contener una o varias moléculas.

### Molecule
- **name**: Nombre de la molécula.
- **creation_date**: Fecha en que se creó la molécula.
- **Relaciones**: Una molécula puede pertenecer a una o varias bandas.

### Data
- **name**: Nombre del dato. (ej: `Measurement set`). Sirve para filtrar por tipo de dato en la interfaz de usuario.
- **creation_date**: Fecha en que se creó el dato.
- **filepath**: Enlace al archivo de datos. (Ej: `ftp://ftp.cv.nrao.edu/NRAO-staff/rloomis/MAPS/HD_163296/VADP/C2H/robust_0.5/HD_163296_C2H_90GHz_hf2.robust_0.5.30deg_radialProfileNoSurface.txt`)
- **image_link**: Enlace a la imagen, opcional. De existir, se podrá visualizar en la interfaz de usuario.
- **size_in_mb**: Tamaño del archivo en MB, opcional.
  - El tamaño del archivo sirve para ser indicado en el script de descarga de datos que los usuarios generan.
- **Relaciones**: Cada dato está asociado a una región, un disco, una banda y una molécula específicos.

## Modelos de `content_management/models.py`

### CarouselImage
Corresponde a las imágenes que se muestran en el carrusel de la página principal.
- **image**: Imagen del carrusel.
- **title**: Título de la imagen.
- **description**: Descripción de la imagen.
- **creation_date**: Fecha en que se creó la imagen.

### Publication
- **title**: Título de la publicación.
- **authors**: Autores de la publicación.
- **full_authors**: Lista completa de autores.
- **journal_info**: Información del journal.
- **summary**: Resumen de la publicación. Debe ser en formato Markdown y se puede visualizar en el BackOffice.
- **image**: Imagen asociada a la publicación.
- **pdf_link**: Enlace al PDF de la publicación.
- **bibtex_link**: Enlace al BibTeX de la publicación.
- **data_link**: Enlace a los datos de la publicación.
- **sao_nasa_link**: Enlace a la base de datos SAO/NASA.

### PressNews
- **content**: Contenido de la noticia. Debe ser en formato Markdown y se puede visualizar en el BackOffice.
- **creation_date**: Fecha en que se creó la noticia.
- **news_type**: Tipo de noticia (prensa oficial o AGEPRO en las noticias).
