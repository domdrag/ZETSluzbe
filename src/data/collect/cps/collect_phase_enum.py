from enum import Enum

class CollectPhaseEnum(Enum):
    GITHUB_SYNCHRONIZATION = 0
    CONFIGURE_DAYS_AND_WEEK_SCHEDULE = 1
    EXTRACT_RULES_BY_DRIVER = 2
    CHECK_UPDATE_NEEDED = 3
    SEARCH_LINKS = 4
    DELETE_NECESSARY_DATA = 5
    EXTRACT_RULES = 6
    ADD_DECRYPTED_SERVICES = 7
    ADD_DECRYPTED_SHIFTS = 8
    CONFIGURE_NOTIFICATION_FILES = 9
    SET_NEW_WARNINGS = 10
    PUSH_NEW_UPDATE_INFO = 11
    UPLOAD_DATA = 12
    END = 13

COLLECT_PHASE_OUTPUT_MESSAGE_MAP = {
    CollectPhaseEnum.GITHUB_SYNCHRONIZATION: 'GitHub sinkronizacija',
    CollectPhaseEnum.CONFIGURE_DAYS_AND_WEEK_SCHEDULE: 'Konfiguracija dana i tjednog rasporeda',
    CollectPhaseEnum.EXTRACT_RULES_BY_DRIVER: 'Citanje tjednih sluzbi',
    CollectPhaseEnum.CHECK_UPDATE_NEEDED: 'Odredivanje potrebe azuriranja',
    CollectPhaseEnum.SEARCH_LINKS: 'Trazenje linkova',
    CollectPhaseEnum.DELETE_NECESSARY_DATA: 'Brisanje potrebnih podataka',
    CollectPhaseEnum.EXTRACT_RULES: 'Citanje svih sluzbi',
    CollectPhaseEnum.ADD_DECRYPTED_SERVICES: 'Spremanje tjednih sluzbi',
    CollectPhaseEnum.ADD_DECRYPTED_SHIFTS: 'Spremanje tjednih smjena',
    CollectPhaseEnum.CONFIGURE_NOTIFICATION_FILES: 'Konfiguracija notifikacija',
    CollectPhaseEnum.SET_NEW_WARNINGS: 'Spremanje novih upozorenja',
    CollectPhaseEnum.PUSH_NEW_UPDATE_INFO: 'Spremanje podataka azuriranja',
    CollectPhaseEnum.UPLOAD_DATA: 'Prijenos podataka na GitHub',
    CollectPhaseEnum.END: 'Sluzbe azurirane!'
}

