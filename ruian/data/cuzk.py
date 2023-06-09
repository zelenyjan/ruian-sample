from __future__ import annotations

import csv
from io import StringIO

import requests
from ruian.data.models import City, District, OrpEntity, PouEntity, Region


def get_data_from_cuzk_and_create_city_instance(city_code) -> City:
    """Get city data from CUZK"""

    url = f"https://vdp.cuzk.cz/vdp/ruian/obce?kodOb={city_code}&search=&mediaType=csv"
    r = requests.get(url)
    r.encoding = "utf-8-sig"
    r.raise_for_status()

    content = StringIO(r.text)

    cr = csv.DictReader(content, delimiter=";")
    # csv should have only one row
    row = next(cr)

    city_code = row["Kód"]
    city_name = row["Název Obce"]
    pou_code = row["Kód POU"]
    pou_name = row["Název POU"]
    orp_code = row["Kód ORP"]
    orp_name = row["Název ORP"]
    district_code = row["Kód Okresu"]
    district_name = row["Název Okresu"]
    region_code = row["Kód Kraje (VÚSC)"]
    region_name = row["Název Kraje (VÚSC)"]

    if pou_code:
        pou, _ = PouEntity.objects.get_or_create(code=pou_code, defaults={"name": pou_name})
    else:
        pou = None

    if orp_code:
        orp, _ = OrpEntity.objects.get_or_create(code=orp_code, defaults={"name": orp_name})
    else:
        orp = None

    region, _ = Region.objects.get_or_create(code=region_code, defaults={"name": region_name})

    if district_code:
        district, _ = District.objects.get_or_create(
            code=district_code, defaults={"name": district_name, "region": region}
        )
    else:
        district = None

    city = City.objects.create(
        code=city_code,
        name=city_name,
        pou=pou,
        orp=orp,
        district=district,
    )

    return city
