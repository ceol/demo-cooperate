from django.db import models


AD_TYPE_0011 = "0011"
AD_TYPE_1011 = "1011"
AD_TYPE_1111 = "1111"
AD_TYPE_1010 = "1010"

AD_TYPES = (
    (AD_TYPE_0011, "Type 0011"),
    (AD_TYPE_1011, "Type 1011"),
    (AD_TYPE_1111, "Type 1111"),
    (AD_TYPE_1010, "Type 1010"),
)

AD_RATES = {
    AD_TYPE_0011: .50,
    AD_TYPE_1011: 1.0,
    AD_TYPE_1111: .75,
    AD_TYPE_1010: .90,
}

AD_SPENDS = {
    AD_TYPE_0011: 200,
    AD_TYPE_1011: 1000,
    AD_TYPE_1111: 500,
    AD_TYPE_1010: 750,
}


class Ad(models.Model):
    ad_type = models.CharField(max_length=4, choices=AD_TYPES)
    spend = models.PositiveSmallIntegerField()
    rate = models.DecimalField(max_digits=3, decimal_places=2)
