"""FIX GATEWAY"""
import sys
import quickfix
from application import Application
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

fix_app = Application()

def main():
    """Main"""
    try:
        print("Init>>>>>")
        settings = quickfix.SessionSettings("client.cfg", True)
        storefactory = quickfix.PostgreSQLStoreFactory(settings)
        logfactory = quickfix.PostgreSQLLogFactory(settings)
        initiator = quickfix.SocketInitiator(fix_app, storefactory, settings, logfactory)

        initiator.start()
        app.run(host="0.0.0.0", port=8080, debug=True)
        initiator.stop()

    except (quickfix.ConfigError, quickfix.RuntimeError) as e:
        print(e)
        # initiator.stop()
        sys.exit()


@app.route('/send_fix_message', methods=['POST'])
def send_fix_message():
    try:
        # print("Start request", flush=True)
        app.logger.info('Start request')
        # Send the FIX message
        order = fix_app.queryNewOrderSingle42()
        fix_app.executeOrder(order)
        # Wait for the response
        fix_app.response_event.wait()
        return jsonify({'success': True, 'message': 'FIX message sent successfully'})
    except Exception as e:
        app.logger.error(e)
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='FIX Client')
    # parser.add_argument('file_name', type=str, help='Name of configuration file')
    # args = parser.parse_args()
    main()
