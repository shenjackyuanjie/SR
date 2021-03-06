"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import os
import sys
import time
import logging
# share memory
from multiprocessing import Manager as share

sys.path.append('./bin/libs/')
sys.path.append('./')
try:
    from bin import tools
    from bin import client
    from bin import server
    from bin import configs
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools
    import client
    import server
    import configs


class Game:

    def __init__(self):
        # basic config
        self.on_python_v_info = sys.version_info
        self.on_python_v = sys.version.split(' ')[0]
        self.start_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))

        # share memory
        self.dicts = share().dict()
        self.lists = share().list()
        # lang_config
        self.language = tools.config('configs/sys_value/basic_config.json5')
        self.language = self.language['language']
        self.lang = tools.config('configs/sys_value/lang/%s.json5' % self.language, 'main')
        # logger
        self.log_config = tools.config('configs/logging.json5', 'file')
        self.log_filename = configs.name_handler(self.log_config['filename']['main'],
                                                 {'date': self.log_config['date_fmt']})
        self.root_logger_fmt = logging.Formatter(self.log_config['fmt'], self.log_config['date_fmt'])
        self.root_logger_stream_handler = logging.StreamHandler()
        self.root_logger_stream_handler.setLevel(self.log_config['level'])
        self.root_logger_stream_handler.setFormatter(self.root_logger_fmt)
        self.root_logger_stream_handler.setLevel(tools.log_level(self.log_config['level']))
        try:
            self.root_logger_file_handler = logging.FileHandler('logs/' + self.log_filename, encoding='utf-8')
        except FileNotFoundError:
            os.mkdir('./logs')
            self.root_logger_file_handler = logging.FileHandler('logs/' + self.log_filename, encoding='utf-8')
        self.root_logger_file_handler.setFormatter(self.root_logger_fmt)
        self.root_logger_file_handler.setLevel(tools.log_level(self.log_config['level']))
        # root logger setup
        logging.getLogger().setLevel(tools.log_level(self.log_config['level']))
        logging.getLogger().addHandler(self.root_logger_stream_handler)
        logging.getLogger().addHandler(self.root_logger_file_handler)
        # create logger
        self.main_logger = logging.getLogger().getChild('main')
        self.server_logger = logging.getLogger().getChild('server')
        self.client_logger = logging.getLogger().getChild('client')
        self.main_logger.info(self.lang['logger.created'])
        self.main_logger.info(self.lang['logger.main_done'])
        self.log_configs()
        # version check
        self.python_version_check()
        # client and server
        self.client = client.client(self.client_logger, self.dicts, self.lists, self.language, net_mode='local')
        self.server = server.server(self.lists, self.dicts, self.server_logger, language=self.language,
                                    net_mode='local')

    def log_configs(self):
        self.main_logger.info('%s %s' % (self.lang['logger.language'], self.lang['lang.language']))
        self.main_logger.info('%s %s' % (self.lang['game_start.at'], self.start_time))
        self.main_logger.debug('%s %s' % (self.lang['logger.logfile_name'], self.log_filename))
        self.main_logger.debug('%s %s' % (self.lang['logger.logfile_level'], self.log_config['level']))
        self.main_logger.debug('%s %s' % (self.lang['logger.logfile_fmt'], self.log_config['fmt']))
        self.main_logger.debug('%s %s' % (self.lang['logger.logfile_datefmt'], self.log_config['date_fmt']))

    def python_version_check(self):
        self.main_logger.info('%s %s' % (self.lang['version.now_on'], self.on_python_v))
        if self.on_python_v_info[0] == 2:
            self.main_logger.critical('%s' % self.lang['version.need3+'])
            raise Exception('%s' % self.lang['version.need3+'])
        elif self.on_python_v_info[1] <= 8:
            warning = configs.name_handler(self.lang['version.best3.8+'])
            self.main_logger.warning(warning)

    def start(self):
        # start
        self.client.run()
