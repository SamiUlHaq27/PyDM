import logging


logger = logging.getLogger('PyDM')
logging.basicConfig(
    filename=__file__.replace('loggers.py','')+'logs/pydm.log',
    filemode='w',
    level=logging.NOTSET
    )

logging.getLogger('flet_runtime').disabled = True
logging.getLogger('flet_core').disabled = True
