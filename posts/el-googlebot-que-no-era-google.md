---
title: "El Googlebot que no era Google: dos semanas de registros"
date: 2026-09-13
excerpt: "De cada cinco peticiones con nombre de robot de IA en mi servidor, cuatro venían de la misma máquina cambiando de identidad."
tags: nginx, servidor, seguridad, registros
---

## Por qué miré los registros

En el servidor donde vive esta web vive también otra que llevo para un negocio de
mi familia. Y ahí estaba el primer problema, antes de mirar nada: las dos
compartían un único fichero de registro, y **86.608 de sus 113.941 líneas eran
ilegibles**. No rotas: escritas con un formato que no se puede leer, porque cada
web declara el suyo y algunas lo declaran mal.

Sin eso arreglado, cualquier cifra por web es humo. Así que lo primero fue dar a
cada web su propio registro. A partir de ahí, ya se puede medir.

## Lo que aparece nada más mirar

En las líneas que sí se pueden leer, entre el 30 de agosto y el 13 de septiembre
hay **8.348 peticiones de escaneo**: 853 direcciones distintas pedidas desde 431
direcciones IP distintas. Nadie busca tu contenido: buscan ficheros que no
deberían estar ahí.

Lo más pedido:

- `/.env` — 100 veces
- `/wp-login.php` — 98
- `/.git/config` — 88
- `/.env.local`, `/.env.production`, `/.env.bak`, `/.env.backup`… — entre 30 y 40 cada uno
- `/xmlrpc.php` — 28
- `/.git/HEAD` — 26

El patrón es claro: ficheros de configuración, credenciales, y las puertas
conocidas de WordPress. Ninguno de esos ficheros existe en esta web.

## Siete brotes

Y luego está lo que me hizo sentarme a escribir esto. Siete direcciones IP que no
escanean como los demás: **entran a saco durante un minuto y se van**. Entre las
siete suman 4.213 peticiones.

- **35.204.202.xxx**: 675 peticiones en 66 segundos, del 13 de septiembre a las 4:19 de la mañana.
- **34.21.79.xxx**: 643 peticiones en un solo minuto, el 7 de septiembre.
- **34.73.253.xxx**, **35.234.1.xxx**, **35.229.84.xxx**, **34.90.79.xxx**, **34.182.214.xxx**: entre 423 y 643 cada una, siempre en ráfagas de menos de dos minutos.

*(Las direcciones van con el último número tapado, aquí y en todo el artículo: el dato que
importa es el rango del que vienen, no la máquina exacta.)*

Lo que llama la atención no es el volumen: es que **cada petición de la ráfaga
llega con un navegador distinto**. Esa primera IP usó 405 identificaciones
diferentes en 66 segundos. La segunda, 400. Es la misma máquina cambiándose de
careta en cada intento.

Y no pedían cualquier cosa:

- `/@fs/proc/self/environ` — el truco de leer ficheros del sistema a través del servidor de desarrollo de Vite
- `/@fs/etc/passwd?import&raw??`
- `/static../.env`, `/media../.env` — saltarse el filtro colando el salto de carpeta dentro de una ruta con pinta de fichero estático
- `/fetch?url=http://169.254.169.254/latest/meta-data/iam/...` — la dirección que en las máquinas de AWS devuelve las credenciales del servidor
- `/aws/credentials`, `/.aws/credentials`, `/.git-credentials`, `/.azure/credentials`
- `/download?file=../../../../etc/passwd`, `/read?url=file:///proc/self/environ`
- `/__aws_leak_probe_50b21472__` — una ruta con nombre propio y un número distinto en cada brote

## El disfraz

Aquí está el hallazgo que no esperaba. En esos mismos registros conté 2.226
peticiones con el nombre de un robot de inteligencia artificial: GPTBot,
OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, Amazonbot, Applebot,
Bytespider, Google-Extended.

**1.854 de ellas, el 83%, salieron de los siete brotes.** No era OpenAI leyendo
mis páginas. Era una máquina alquilada por horas cambiando de nombre en cada
petición.

En crudo se ve mejor que explicado:

```
35.204.202.xxx - - [13/Sep/2026:04:19:19 +0000]
  "GET /__aws_leak_probe_50b21472__ HTTP/1.1" 301 178
  "Mozilla/5.0 (compatible; OAI-SearchBot/1.4; robots.txt; +https://openai.com/searchbot)"
```

Hasta el detalle del `robots.txt` que OpenAI documenta para sus lecturas de
`robots.txt` está copiado. Lo que no está copiado es la dirección: pidiendo
`/.env` y credenciales de AWS no hay ninguna razón para llevar el nombre de
OpenAI.

## Google, esta vez sí

Con Google es más fácil, porque se puede comprobar. En esas dos semanas hubo 226
peticiones diciendo ser Googlebot.

- **171** venían del rango `66.249.x`, desde 45 direcciones distintas.
- Y su DNS inverso lo confirma: `66.249.75.xxx` resuelve a `crawl-66-249-75-xxx.googlebot.com`, que es el patrón que Google publica[1].
- Las otras **55** llegaban desde direcciones ajenas a Google. De esas, 28 venían pidiendo `/.env` y compañía.

Es decir: el nombre de Googlebot era Google el 75% de las veces. Los nombres de
los robots de IA, casi nunca.

## Qué se llevaron

Nada. De esas 8.348 peticiones:

- **3.904** recibieron un 404. Ningún fichero existía.
- **4.393** recibieron un 301: entraron por HTTP a la dirección IP y se les mandó a HTTPS, así que ni llegaron a pedirle nada a la aplicación.
- **12** recibieron un 200, y ninguna de las doce es una fuga: diez son las validaciones de Let's Encrypt (el trámite normal cada vez que se renueva el certificado) y dos son la página del área de clientes, que responde a `/portal/.env` con su propia página. Lo he comprobado ahora mismo: 2.291 bytes de HTML, no un fichero de credenciales.
- **2** recibieron un 500, y esas dos sí me interesan: `/dashboard/.env` y `/dashboard%2F.env` hacen fallar la aplicación en vez de responder 404. Es un fallo pequeño y lo voy a arreglar, pero es justo el tipo de detalle que no se ve si no se miran los registros.

Todo lo que pedían, comprobado hoy a mano y por HTTPS, responde 404 en las dos
webs.

## Y la rareza

Hay una petición que no encaja en ninguna de las categorías anteriores. Durante
dos semanas, algo que sale por direcciones de Cloudflare ha pedido
`/wp-admin/install.php?step=1` **2.154 veces**, unas 150 al día, siempre la misma
ruta, y con el campo del navegador puesto a la propia dirección:

```
104.23.221.xxx - - [13/Sep/2026:01:27:15 +0000]
  "GET /wp-admin/install.php?step=1 HTTP/1.1" 301 178 "-"
  "http://jlsw.dev/wp-admin/install.php?step=1"
```

No sé quién hay detrás. Sé que esta web no es WordPress y que ahí no hay nada
que encontrar.

## Cómo saber si un robot es de verdad

La lección es corta: **el nombre no vale, la dirección sí**. Un nombre de
navegador o de robot se escribe en una línea y no cuesta nada; la dirección IP
desde la que llega, no. Google publica sus rangos y el patrón de DNS inverso
(`crawl-…​.googlebot.com`) para comprobarlo en dos comandos[1], y OpenAI publica
los suyos y explica el marcador de `robots.txt`[2].

La comprobación es esta:

```
35.204.202.xxx  -> xxx.202.204.35.bc.googleusercontent.com
66.249.75.xxx   -> crawl-66-249-75-xxx.googlebot.com
```

La primera está en Google Cloud: es una máquina virtual que cualquiera alquila
por horas. La segunda es Google. Y las dos dicen «Google» cuando piden algo.

## Lo que me llevo

Nada estaba expuesto, y no había ninguna brecha: lo que hay es muchísimo ruido,
y un puñado de sitios donde la aplicación se comporta mal (esos dos 500). Ahora
cada web tiene su propio registro, así que la próxima vez que mire esto, las
cifras serán de una sola web y no del servidor entero. Se puede medir mejor,
también esto.

Si tienes una web, mira tu registro. Casi seguro que ese Googlebot que te visita
no es Google.

## Referencias

1. Google — *Verify requests from Google crawlers and fetchers*: https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot
2. OpenAI — *Overview of OpenAI Crawlers*: https://platform.openai.com/docs/gptbot
