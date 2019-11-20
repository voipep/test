#!/usr/bin/env python3

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology.dialogue.intent import IntentMessage


CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


class Test(object):
    """Class used to wrap action code with mqtt connection
       Please change the name referring to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except Exception:
            self.config = None

        # start listening to MQTT
        self.start_blocking()


    @staticmethod
    def intent_1_callback(hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        intentname = intent_message.intent.intent_name
        if intentname == "atesfa:test":
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, "test")

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intent('intent_1', self.intent_1_callback) \
            .loop_forever()


if __name__ == "__main__":
    Test()