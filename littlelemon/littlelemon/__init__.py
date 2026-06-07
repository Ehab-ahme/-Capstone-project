import pymysql

# بأن النسخة هي 2.2.1 لتجاوز فحص الإصدار Django إيهام
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()