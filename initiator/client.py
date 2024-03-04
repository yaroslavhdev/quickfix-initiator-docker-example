"""FIX GATEWAY"""
import sys
import quickfix
from application import Application
from flask import Flask, request, jsonify

app_server = Flask(__name__)
app_fix = Application()

def main():
    """Main"""
    try:
        print("Init")
        settings = quickfix.SessionSettings("client.cfg")
        storefactory = quickfix.PostgreSQLStoreFactory(settings)
        logfactory = quickfix.PostgreSQLLogFactory(settings)
        initiator = quickfix.SocketInitiator(app_fix, storefactory, settings, logfactory)

        initiator.start()
        app_server.run(host="0.0.0.0", port=8080, debug=True)
        initiator.stop()

    except (quickfix.ConfigError, quickfix.RuntimeError) as e:
        print(e)
        # initiator.stop()
        sys.exit()


@app_server.route('/send_fix_message', methods=['POST'])
def send_fix_message():
    try:
        # Send the FIX message
        app_fix.queryNewOrderSingle42()
        # Wait for the response
        app_fix.response_event.wait()
        return jsonify({'success': True, 'message': 'FIX message sent successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__=='__main__':
    # parser = argparse.ArgumentParser(description='FIX Client')
    # parser.add_argument('file_name', type=str, help='Name of configuration file')
    # args = parser.parse_args()
    main()
