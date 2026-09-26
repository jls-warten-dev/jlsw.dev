---
title: "El Googlebot que no era Google: dos semanas de registros"
title_en: "The Googlebot that was not Google: two weeks of logs"
date: 2026-09-13
excerpt: "De cada cinco peticiones con nombre de robot de IA en mi servidor, cuatro venían de la misma máquina cambiando de identidad."
excerpt_en: "Out of every five requests bearing an AI bot name on my server, four came from the same machine changing its identity."
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

- `/.env`, 100 veces
- `/wp-login.php`, 98
- `/.git/config`, 88
- `/.env.local`, `/.env.production`, `/.env.bak`, `/.env.backup`..., entre 30 y 40 cada uno
- `/xmlrpc.php`, 28
- `/.git/HEAD`, 26

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

- `/@fs/proc/self/environ`, el truco de leer ficheros del sistema a través del servidor de desarrollo de Vite
- `/@fs/etc/passwd?import&raw??`
- `/static../.env`, `/media../.env`, saltarse el filtro colando el salto de carpeta dentro de una ruta con pinta de fichero estático
- `/fetch?url=http://169.254.169.254/latest/meta-data/iam/...`, la dirección que en las máquinas de AWS devuelve las credenciales del servidor
- `/aws/credentials`, `/.aws/credentials`, `/.git-credentials`, `/.azure/credentials`
- `/download?file=../../../../etc/passwd`, `/read?url=file:///proc/self/environ`
- `/__aws_leak_probe_50b21472__`, una ruta con nombre propio y un número distinto en cada brote

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
(`crawl-...​.googlebot.com`) para comprobarlo en dos comandos[1], y OpenAI publica
los suyos y explica el marcador de `robots.txt`[2].

La comprobación es esta:

```
35.204.202.xxx -> xxx.202.204.35.bc.googleusercontent.com
66.249.75.xxx -> crawl-66-249-75-xxx.googlebot.com
```

La primera está en Google Cloud: es una máquina virtual que cualquiera alquila
por horas. La segunda es Google. Y las dos dicen "Google" cuando piden algo.

## Lo que me llevo

Nada estaba expuesto, y no había ninguna brecha: lo que hay es muchísimo ruido,
y un puñado de sitios donde la aplicación se comporta mal (esos dos 500). Ahora
cada web tiene su propio registro, así que la próxima vez que mire esto, las
cifras serán de una sola web y no del servidor entero. Se puede medir mejor,
también esto.

Si tienes una web, mira tu registro. Casi seguro que ese Googlebot que te visita
no es Google.

## Referencias

1. Google, *Verify requests from Google crawlers and fetchers*: https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot
2. OpenAI, *Overview of OpenAI Crawlers*: https://platform.openai.com/docs/gptbot

<!-- :en -->

## Why I looked at the logs

The server where this site lives also hosts another one I run for a family
business. And there was the first problem, before looking at anything: the two
shared a single log file, and **86,608 of its 113,941 lines were unreadable**.
Not corrupt: written in a format that cannot be read, because every site declares
its own and some declare it badly.

Without fixing that, any figure per site is smoke. So the first thing was giving
each site its own log. From there on, you can actually measure.

## What shows up as soon as you look

In the lines that can be read, between 30 August and 13 September there are
**8,348 scanning requests**: 853 different addresses requested from 431 different
IP addresses. Nobody is looking for your content: they are looking for files that
should not be there.

The most requested:

- `/.env`, 100 times
- `/wp-login.php`, 98
- `/.git/config`, 88
- `/.env.local`, `/.env.production`, `/.env.bak`, `/.env.backup`..., between 30 and 40 each
- `/xmlrpc.php`, 28
- `/.git/HEAD`, 26

The pattern is clear: configuration files, credentials, and the well known
WordPress doors. None of those files exist on this site.

## Seven bursts

And then there is what made me sit down and write this. Seven IP addresses that do
not scan like the others: **they go in hard for a minute and leave**. Between the
seven of them they add up to 4,213 requests.

- **35.204.202.xxx**: 675 requests in 66 seconds, on 13 September at 4:19 in the morning.
- **34.21.79.xxx**: 643 requests in a single minute, on 7 September.
- **34.73.253.xxx**, **35.234.1.xxx**, **35.229.84.xxx**, **34.90.79.xxx**, **34.182.214.xxx**: between 423 and 643 each, always in bursts of under two minutes.

*(The addresses have their last number masked, here and throughout the article: the
data that matters is the range they come from, not the exact machine.)*

What stands out is not the volume: it is that **every request in the burst arrives
with a different browser**. That first IP used 405 different identifications in 66
seconds. The second one, 400. It is the same machine changing masks on every attempt.

And they were not asking for just anything:

- `/@fs/proc/self/environ`, the trick of reading system files through the Vite development server
- `/@fs/etc/passwd?import&raw??`
- `/static../.env`, `/media../.env`, slipping past the filter by hiding the directory jump inside a path that looks like a static file
- `/fetch?url=http://169.254.169.254/latest/meta-data/iam/...`, the address that on AWS machines returns the server credentials
- `/aws/credentials`, `/.aws/credentials`, `/.git-credentials`, `/.azure/credentials`
- `/download?file=../../../../etc/passwd`, `/read?url=file:///proc/self/environ`
- `/__aws_leak_probe_50b21472__`, a path with its own name and a different number in every burst

## The disguise

Here is the finding I was not expecting. In those same logs I counted 2,226
requests bearing the name of an artificial intelligence robot: GPTBot,
OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, Amazonbot, Applebot,
Bytespider, Google-Extended.

**1,854 of them, 83%, came from the seven bursts.** It was not OpenAI reading my
pages. It was a machine rented by the hour changing its name on every request.

It reads better raw than explained:

```
35.204.202.xxx - - [13/Sep/2026:04:19:19 +0000]
 "GET /__aws_leak_probe_50b21472__ HTTP/1.1" 301 178
 "Mozilla/5.0 (compatible; OAI-SearchBot/1.4; robots.txt; +https://openai.com/searchbot)"
```

Even the `robots.txt` detail that OpenAI documents for its `robots.txt` reads is
copied. What is not copied is the address: asking for `/.env` and AWS credentials
there is no reason whatsoever to carry OpenAI's name.

## Google, this time yes

With Google it is easier, because it can be checked. In those two weeks there were
226 requests claiming to be Googlebot.

- **171** came from the `66.249.x` range, from 45 different addresses.
- And their reverse DNS confirms it: `66.249.75.xxx` resolves to `crawl-66-249-75-xxx.googlebot.com`, which is the pattern Google publishes[1].
- The other **55** arrived from addresses outside Google. Of those, 28 came asking for `/.env` and friends.

That is: the name Googlebot was Google 75% of the time. The names of the AI
robots, almost never.

## What they got away with

Nothing. Out of those 8,348 requests:

- **3,904** received a 404. No file existed.
- **4,393** received a 301: they came in over HTTP to the IP address and were sent to HTTPS, so they never got to ask the application for anything.
- **12** received a 200, and none of the twelve is a leak: ten are Let's Encrypt validations (the normal routine every time the certificate is renewed) and two are the client area page, which answers `/portal/.env` with its own page. I checked it just now: 2,291 bytes of HTML, not a credentials file.
- **2** received a 500, and those two do interest me: `/dashboard/.env` and `/dashboard%2F.env` make the application fail instead of answering 404. It is a small fault and I am going to fix it, but it is exactly the kind of detail you do not see unless you look at the logs.

Everything they asked for, checked today by hand and over HTTPS, answers 404 on
both sites.

## And the oddity

There is one request that does not fit any of the previous categories. For two
weeks, something coming out of Cloudflare addresses has asked for
`/wp-admin/install.php?step=1` **2,154 times**, about 150 a day, always the same
path, and with the browser field set to the address itself:

```
104.23.221.xxx - - [13/Sep/2026:01:27:15 +0000]
 "GET /wp-admin/install.php?step=1 HTTP/1.1" 301 178 "-"
 "http://jlsw.dev/wp-admin/install.php?step=1"
```

I do not know who is behind it. I do know this site is not WordPress and there is
nothing to find there.

## How to tell whether a bot is real

The lesson is short: **the name is worthless, the address is what counts**. A
browser or bot name is written in one line and costs nothing; the IP address it
arrives from does not. Google publishes its ranges and the reverse DNS pattern
(`crawl-....googlebot.com`) to check it in two commands[1], and OpenAI publishes
its own and explains the `robots.txt` token[2].

The check is this:

```
35.204.202.xxx -> xxx.202.204.35.bc.googleusercontent.com
66.249.75.xxx -> crawl-66-249-75-xxx.googlebot.com
```

The first one is on Google Cloud: it is a virtual machine anyone can rent by the
hour. The second is Google. And both say "Google" when they ask for something.

## What I take away

Nothing was exposed, and there was no breach: what there is is an enormous amount
of noise, and a handful of places where the application behaves badly (those two
500s). Now each site has its own log, so the next time I look at this the figures
will be for a single site and not the whole server. This can be measured better too.

If you have a website, look at your log. Almost certainly that Googlebot visiting
you is not Google.

## References

1. Google, *Verify requests from Google crawlers and fetchers*: https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot
2. OpenAI, *Overview of OpenAI Crawlers*: https://platform.openai.com/docs/gptbot
