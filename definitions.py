

"""
Model-Mapping as provided at: https://psm.tech4germany.org/#/default/get_schadorg_gruppe_
-> Model
-> Removing the second "type-like column"

Map Description:
-----------------
Table-Name : String with Model definition
For each Table-Name, there must be exactly one endpoint in the endpoint
map provided below.

Model-Definition:
------------------
Important: One Definition per Line, no empty line allowed!
<Column-Name> <whitespaces> <Column-Type>

Type-Mappings (which types are known/allowed and map to which sqlite-type) are provided
at generator.TYPE_MAP
"""

definition = {
    "STAND": """DATUM   DATE
    M_ROW$$     VARCHAR2""",

    "AWG": """ANTRAGNR	VARCHAR2
    ANWENDUNGEN_ANZ_JE_BEFALL	NUMBER
    ANWENDUNGEN_MAX_JE_KULTUR	NUMBER
    ANWENDUNGEN_MAX_JE_VEGETATION	NUMBER
    ANWENDUNGSBEREICH	VARCHAR2
    ANWENDUNGSTECHNIK	VARCHAR2
    AWGNR	VARCHAR2
    AWG_ID	VARCHAR2
    AW_ABSTAND_BIS	NUMBER
    AW_ABSTAND_EINHEIT	VARCHAR2
    AW_ABSTAND_VON	NUMBER
    EINSATZGEBIET	VARCHAR2
    GENEHMIGUNG	CHAR
    HUK	CHAR
    KENNR	VARCHAR2
    KULTUR_ERL	VARCHAR2
    M_ROW$$	VARCHAR2
    SCHADORG_ERL	VARCHAR2
    STADIUM_KULTUR_BEM	VARCHAR2
    STADIUM_KULTUR_BIS	VARCHAR2
    STADIUM_KULTUR_KODELISTE	NUMBER
    STADIUM_KULTUR_VON	VARCHAR2
    STADIUM_SCHADORG_BEM	VARCHAR2
    STADIUM_SCHADORG_BIS	VARCHAR2
    STADIUM_SCHADORG_KODELISTE	NUMBER
    STADIUM_SCHADORG_VON	VARCHAR2
    WIRKUNGSBEREICH	VARCHAR2""",

    "AUFLAGEN": """ABSTAND	NUMBER
    ANWENDBEST	CHAR
    ANWENDUNGSTECHNIK	VARCHAR2
    AUFLAGE	VARCHAR2
    AUFLAGENR	NUMBER
    EBENE	VARCHAR2
    KULTUR	VARCHAR2
    M_ROW$$	VARCHAR2
    REDU_ABSTAND	VARCHAR2
    WEITERE_BEDINGUNG	VARCHAR2""",

    "AUFLAGE_REDU": """AUFLAGENR	NUMBER
    KATEGORIE	VARCHAR2
    M_ROW$$	VARCHAR2
    REDU_ABSTAND	VARCHAR2""",
    
    "KODE": """KODE	VARCHAR2
    KODELISTE	NUMBER
    KODETEXT	VARCHAR2
    SPERRE	CHAR
    SPRACHE	VARCHAR2""",

    "AWG_AUFWAND": """AUFWANDBEDINGUNG	VARCHAR2
    AWG_ID	VARCHAR2
    M_AUFWAND	NUMBER
    M_AUFWAND_EINHEIT	VARCHAR2
    M_ROW$$	VARCHAR2
    SORTIER_NR	NUMBER
    W_AUFWAND_BIS	NUMBER
    W_AUFWAND_EINHEIT	VARCHAR2
    W_AUFWAND_VON	NUMBER""",
    
    "KULTUR_GRUPPE": """KULTUR	VARCHAR2
    KULTUR_GRUPPE	VARCHAR2
    M_ROW$$	VARCHAR2""",
    
    "AWG_ZEITPUNKT": """AWG_ID	VARCHAR2
    M_ROW$$	VARCHAR2
    OPERAND_ZU_VORHER	VARCHAR2
    SORTIER_NR	NUMBER
    ZEITPUNKT	VARCHAR2""",
    
    "SCHADORG_GRUPPE": """M_ROW$$	VARCHAR2
    SCHADORG	VARCHAR2
    SCHADORG_GRUPPE	VARCHAR2"""
}

"""
Definition of the Endpoints. Name of the Endpoint must be found in the
definition map above.

Format: "<endpoint>/?offset="
"""
endpoints = {
    "STAND": "https://psm-api.bvl.bund.de/ords/psm/api-v1/stand/?offset=",
    "AWG": "https://psm-api.bvl.bund.de/ords/psm/api-v1/awg/?offset=",
    "AUFLAGEN": "https://psm-api.bvl.bund.de/ords/psm/api-v1/auflagen/?offset=",
    "AUFLAGE_REDU": "https://psm-api.bvl.bund.de/ords/psm/api-v1/auflage_redu/?offset=",
    "KODE": "https://psm-api.bvl.bund.de/ords/psm/api-v1/kode/?offset=",
    "AWG_AUFWAND": "https://psm-api.bvl.bund.de/ords/psm/api-v1/awg_aufwand/?offset=",
    "KULTUR_GRUPPE": "https://psm-api.bvl.bund.de/ords/psm/api-v1/kultur_gruppe/?offset=",
    "AWG_ZEITPUNKT": "https://psm-api.bvl.bund.de/ords/psm/api-v1/awg_zeitpunkt/?offset=",
    "SCHADORG_GRUPPE": "https://psm-api.bvl.bund.de/ords/psm/api-v1/schadorg_gruppe/?offset="
}
