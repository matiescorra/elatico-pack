# Pack de El Ático

Pack de recursos del servidor de Minecraft de **El Ático** (San Luis). El server lo manda solo al entrar: los jugadores no tienen que instalar nada, y es opcional.

## Qué trae
- **Moneda ATIPESO**: el símbolo ₳ se reemplaza por la moneda de Atiquín en el chat, los carteles de tienda, el tablón y `/dinero`. Quien rechace el pack sigue viendo ₳.
- **Ítem `elatico:atipeso`**: modelo para monedas físicas (premios, eventos).
- **Cosméticos de raza** (v4): orejas, barba, cuernos, alas, capucha, cola… en `elatico:cosmetico/<raza>_<cabeza|cuerpo>`. Se generan con `herramientas/cosmeticos.py` (vista previa: `vista_cosmeticos.py`).

## Estructura
| Carpeta | Qué hay |
|---|---|
| `fuente/` | El pack sin comprimir. Acá se edita. |
| `packs/` | Los .zip versionados que descarga el server (`ElAtico-v1.zip`, `-v2`...). **No se borran** versiones viejas. |
| `herramientas/` | Scripts para generar texturas (ej. `moneda.py`). |

## Cómo sacar una versión nueva
1. Editar lo que haga falta en `fuente/`.
2. Comprimir el *contenido* de `fuente/` (que `pack.mcmeta` quede en la raíz del zip) como `packs/ElAtico-vN.zip`.
3. Calcular el SHA-1 del zip.
4. En el server, `plugins/AticoCore/config.yml` → sección `pack-atico`: actualizar `url` y `sha1`, y reiniciar.

Link de descarga: `https://raw.githubusercontent.com/matiescorra/elatico-pack/main/packs/ElAtico-vN.zip`

Formato: Minecraft 26.2 (pack format 88), compatible desde 1.21.4.
