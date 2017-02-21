# First File

from cm_api.api_client import ApiResource
import ConfigParser
import sys

# ------------------------------------------------------------------------------------------


global Config, cluster, api

# ------------------------------------------------------------------------------------------


def read_conf():

    global Config
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    print("\n[INFO] : " + str(len(Config.sections())) +
          " cluster detected on the config file")
    return Config.sections()

# ------------------------------------------------------------------------------------------


def get_cluster(cm_host, user,
                pwd, cluster_name):

    global api
    api = ApiResource(cm_host, username=user, password=pwd, version=12)
    for c in api.get_all_clusters():
        if cluster_name in c.name:
            # print("Cluster, Version : " + c.name + ", " + c.version)
            return True, c
        else:
            print("[ERR] : Cluster \"" + cluster_name
                  + "\" not found at \"" + cm_host + "\"")
            return False, ""

# ------------------------------------------------------------------------------------------


def get_service_status(cluster_alias, this_cluster):

    # this_cluster_name = this_cluster.name
    output = open("t.txt", "w")
    print cluster_alias + "," + "cluster" + "," + this_cluster.entityStatus.split("_")[0] \
          + "," + str(this_cluster.maintenanceMode).upper()
    output.write(cluster_alias + "," + "cluster" + "," + this_cluster.entityStatus.split("_")[0] + "," \
          + str(this_cluster.maintenanceMode).upper() + "\n")
    for s in this_cluster.get_all_services():
        # print s
        if s.type != "TEST":
            hdfs_ser = s
            print(cluster_alias + "," + hdfs_ser.name + "," + hdfs_ser.serviceState + "," + hdfs_ser.healthSummary
                  + "," + str(hdfs_ser.maintenanceMode).upper())
            output.write(cluster_alias + "," + hdfs_ser.name + "," + hdfs_ser.serviceState + ","
                         + hdfs_ser.healthSummary + "," + str(hdfs_ser.maintenanceMode).upper() + "\n")
    output.close()

# ------------------------------------------------------------------------------------------


# Function Calls and Program Flow


def logic():

    print("Call Received")
    count = 0

    try:
        # Read Configuration
        instances = read_conf()
        for c in instances:

            alias = Config.get(c, 'alias')
            h = Config.get(c, 'cm_host')
            u = Config.get(c, 'user')
            p = Config.get(c, 'pwd')
            cn = Config.get(c, 'cluster_name')
            count += 1

            print("\n### " + str(count) + "/" + str(len(instances)) + " : " + alias)

            try:
                # Connect to Cluster
                services, cluster_ref = get_cluster(h, u, p, cn)
                if services:

                    try:
                        # Fetch Service Status
                        get_service_status(alias, cluster_ref)

                    except:
                        print("[ERR] : Can't fetch services :: " + str(sys.exc_info()[0]))

            except:
                print("[ERR] : Can't Connect to Cluster :: " + str(sys.exc_info()[0]))

    except:
        print("[ERR] : Can't Read Configuration! :: " + str(sys.exc_info()[0]))

# ------------------------------------------------------------------------------------------
