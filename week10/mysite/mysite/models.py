from django.db import models


class TestCase(models.Model):
    pass


# 从数据库反向生成的模型
class TApplication(models.Model):
    application_id = models.IntegerField(primary_key=True)
    application_name = models.CharField(max_length=100)
    application_type = models.IntegerField(blank=True, null=True)
    person_of_primary = models.CharField(max_length=20, blank=True, null=True)
    receiving_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    cluster_mode = models.CharField(max_length=100, blank=True, null=True)
    ip_group_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_application'


class TTestGroup(models.Model):
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    group_id = models.CharField(primary_key=True, max_length=32)
    group_name = models.CharField(max_length=128, blank=True, null=True)
    group_desc = models.CharField(max_length=256, blank=True, null=True)
    interval = models.IntegerField(blank=True, null=True)
    multi_thread = models.IntegerField(blank=True, null=True)
    mode = models.CharField(max_length=32, blank=True, null=True)
    severity = models.CharField(max_length=32, blank=True, null=True)
    touser = models.CharField(max_length=32, blank=True, null=True)
    toparty = models.CharField(max_length=32, blank=True, null=True)
    totag = models.CharField(max_length=32, blank=True, null=True)
    fail_threshold = models.IntegerField(blank=True, null=True)
    check_count = models.IntegerField(blank=True, null=True)
    recovery_threshold = models.IntegerField(blank=True, null=True)
    recovery_check_count = models.IntegerField(blank=True, null=True)
    agentid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_test_group'


class TTestCase(models.Model):
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    req_method = models.CharField(max_length=32, blank=True, null=True)
    req_header = models.CharField(max_length=1024, blank=True, null=True)
    url_param = models.CharField(max_length=1024, blank=True, null=True)
    req_body = models.CharField(max_length=1024, blank=True, null=True)
    exp_result = models.CharField(max_length=256, blank=True, null=True)
    case_id = models.CharField(max_length=32, blank=True, null=True)
    group_id = models.CharField(max_length=32, blank=True, null=True)
    application_id = models.IntegerField(blank=True, null=True)
    case_name = models.CharField(max_length=256, blank=True, null=True)
    case_desc = models.CharField(max_length=1024, blank=True, null=True)
    server_list = models.CharField(max_length=256, blank=True, null=True)
    test_mode = models.CharField(max_length=32, blank=True, null=True)
    url = models.CharField(max_length=1024, blank=True, null=True)
    severity = models.CharField(max_length=32, blank=True, null=True)
    touser = models.CharField(max_length=32, blank=True, null=True)
    toparty = models.CharField(max_length=32, blank=True, null=True)
    totag = models.CharField(max_length=32, blank=True, null=True)

    # detail = models.OneToOneField("TApplication", to_field="application_id", on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = 't_test_case'


class TTestResult(models.Model):
    test_id = models.CharField(max_length=32, blank=True, null=True)
    task_id = models.CharField(max_length=36, blank=True, null=True)
    group_id = models.CharField(max_length=36, blank=True, null=True)
    case_id = models.CharField(max_length=32, blank=True, null=True)
    server = models.CharField(max_length=32, blank=True, null=True)
    rsp_code = models.CharField(max_length=32, blank=True, null=True)
    rsp_data = models.CharField(max_length=2048, blank=True, null=True)
    test_status = models.IntegerField(blank=True, null=True)
    start_time = models.CharField(max_length=26, blank=True, null=True)
    end_time = models.CharField(max_length=26, blank=True, null=True)
    spend = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=2048, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_test_result'