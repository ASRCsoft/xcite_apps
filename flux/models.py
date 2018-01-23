# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Nysmesonet(models.Model):
    datetime = models.DateTimeField(primary_key=True)
    stid = models.ForeignKey('Sites', models.DO_NOTHING, db_column='stid')
    wd_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fetch_90 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h2o_density_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_hfp01_3 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    co2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    t_sonic_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ta_1_1_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tau = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pa = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    t_nr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tau_qc = models.SmallIntegerField(blank=True, null=True)
    u_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h2o = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tke = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rn = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    t_dp_1_1_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    co2_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bowen_ratio = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lws_volt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_hfp01_4 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tstar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ws_rslt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    upwnd_dist_intrst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_hfp01_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    zl = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ftprnt_dist_intrst = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    le = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sw_in = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wd = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_hfp01_2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h_qc = models.SmallIntegerField(blank=True, null=True)
    fc_mass = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h2o_sig_strgth_min = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ftprnt_equation = models.TextField(blank=True, null=True)
    ws = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wd_sonic = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sonic_azimuth = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fc_qc = models.SmallIntegerField(blank=True, null=True)
    fc_samples_tot = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rh_1_1_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    le_qc = models.SmallIntegerField(blank=True, null=True)
    co2_density_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ws_max = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_out = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    w = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ustar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h2o_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    alb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mo_length = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fetch_55 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    vpd = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    co2_sig_strgth_min = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sw_out = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    w_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h2o_density_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fetch_max = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    le_samples_tot = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pa_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    t_sonic = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    v = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_in = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fetch_40 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    v_sigma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_6cm = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ta_sigma_1_1_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h_samples_tot = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    co2_density_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    u = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    r_sw_out_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    chargestate = models.TextField(blank=True, null=True)
    solarpanels_on_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    full_ec_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ts_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sw_in_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    le_ssitc_test = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    i_in_chg_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    t_nr_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    h_ssitc_test = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nr_ventilator_state_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nr_heater_state_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nr_tachometer_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pump_tmpr_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ec100_relay_state_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    netrad_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    low_power_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sys_watts_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    checkbattery = models.TextField(blank=True, null=True)
    lws_status = models.TextField(blank=True, null=True)
    chargesource = models.TextField(blank=True, null=True)
    ec155_off_flg_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    standby_ec_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cell_tmpr_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fc_ssitc_test = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    r_lw_in_meas_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    runavgsw_in_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    runavglws_volt_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    r_sw_in_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    r_lw_out_meas_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    batt_volt_cr6_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    v_in_chg_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ibatt_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    albedo_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cdm_pwr_state_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    intake_heater_pwr_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    chg_tmpc_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    r_lw_in_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    r_lw_out_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    iload_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tau_ssitc_test = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    vbatt_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    valve_tmpr_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_plate_4_1_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_plate_3_1_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_plate_1_1_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g_plate_2_1_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    g = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    energy_closure = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    r_rn_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nr_fan_state_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    v_in_cr6_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    chg_tmpr_avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    full_ec = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ec100_relay_state = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cdm_pwr_state = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    low_power = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    standby_ec = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ec155_off_flg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nr_ventilator_state = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nr_heater_state = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    solarpanels_on = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nysmesonet'
        unique_together = (('datetime', 'stid'),)


class Sites(models.Model):
    stid = models.CharField(primary_key=True, max_length=255)
    number = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    nearest_city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    distance_from_town = models.FloatField(blank=True, null=True)
    direction_from_town = models.CharField(max_length=255, blank=True, null=True)
    climate_division = models.SmallIntegerField(blank=True, null=True)
    climate_division_name = models.CharField(max_length=255, blank=True, null=True)
    wfo = models.CharField(max_length=255, blank=True, null=True)
    commissioned = models.DateTimeField(blank=True, null=True)
    decommissioned = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sites'

# need a router to make sure these go to the right place
class FluxRouter(object):
    apps = ['flux']
    def __init__(self):
        # just want to have the apps associated with the lidar
        # database here so I can control all of them in one place
        self.apps =['flux']
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.apps:
            return 'flux'
        return None
    def db_for_write(self, model, **hints):
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.apps or \
           obj2._meta.app_label in self.apps:
           return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'flux':
            return False
        return None
