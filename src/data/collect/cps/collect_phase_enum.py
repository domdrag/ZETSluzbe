from enum import Enum

class CollectPhaseEnum(Enum):
    CONFIGURE_DAYS_AND_WEEK_SCHEDULE = 0
    EXTRACT_RULES_BY_DRIVER = 1
    CHECK_UPDATE_NEEDED = 2
    SEARCH_LINKS = 3
    DELETE_NECESSARY_DATA = 4
    EXTRACT_RULES = 5
    ADD_DECRYPTED_SERVICES = 6
    ADD_DECRYPTED_SHIFTS = 7
    CONFIGURE_NOTIFICATION_FILES = 8
    SET_NEW_CONFIG_AND_WARNINGS = 9
    PREPARE_DATA_FOR_TRANSPORT = 10
    UPLOAD_CLIENT_DATA = 11
    UPLOAD_DATA_TO_DROPBOX = 12
    END = 13

COLLECT_PHASE_OUTPUT_MESSAGE_MAP = {
    CollectPhaseEnum.CONFIGURE_DAYS_AND_WEEK_SCHEDULE: 'Konfiguracija dana i tjednog rasporeda',
    CollectPhaseEnum.EXTRACT_RULES_BY_DRIVER: 'Citanje tjednih sluzbi',
    CollectPhaseEnum.CHECK_UPDATE_NEEDED: 'Odredivanje potrebe azuriranja',
    CollectPhaseEnum.SEARCH_LINKS: 'Trazenje linkova',
    CollectPhaseEnum.DELETE_NECESSARY_DATA: 'Brisanje potrebnih podataka',
    CollectPhaseEnum.EXTRACT_RULES: 'Citanje svih sluzbi',
    CollectPhaseEnum.ADD_DECRYPTED_SERVICES: 'Spremanje tjednih sluzbi',
    CollectPhaseEnum.ADD_DECRYPTED_SHIFTS: 'Spremanje tjednih smjena',
    CollectPhaseEnum.CONFIGURE_NOTIFICATION_FILES: 'Konfiguracija notifikacija',
    CollectPhaseEnum.SET_NEW_CONFIG_AND_WARNINGS: 'Spremanje nove konfiguracije',
    CollectPhaseEnum.PREPARE_DATA_FOR_TRANSPORT: 'Pripremanje podataka za transport',
    CollectPhaseEnum.UPLOAD_CLIENT_DATA: 'Ucitavanje sluzbi na Github',
    CollectPhaseEnum.UPLOAD_DATA_TO_DROPBOX: 'Ucitavanje sluzbi na Dropbox',
    CollectPhaseEnum.END: 'Sluzbe azurirane!'
}

