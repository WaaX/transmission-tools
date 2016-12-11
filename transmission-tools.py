import argparse
import transmissionrpc


class TransmissionTools(object):

    @staticmethod
    def build_using_address(address, port=9091):
        return TransmissionTools(transmissionrpc.Client(address, port))

    def __init__(self, client):
        self.client = client

    def _uncheck_file_if_match(self, method):
        for torrent in self.client.get_torrents():
            to_remove = [file_index for file_index, file_torrent in torrent.files().iteritems() if method(file_torrent)] 
            if to_remove:
                self.client.change_torrent(torrent.hashString, files_unwanted=to_remove)


    def uncheck_sample(self):
        self._uncheck_file_if_match(lambda file_torrent: 'sample' in file_torrent['name'].lower())

    def uncheck_advertisement(self):
        def validate_filename(file_torrent):
	    patterns = ['www.Speed.Cd.txt', 'downloaded from', 'RARBG.com.txt', 'www.Torrenting.com.txt', 'www.Speed.Cd read me .txt']
	    return any(pattern in file_torrent['name'] for pattern in patterns)
        self._uncheck_file_if_match(validate_filename)

    def remove_completed(self):
        pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Transmission-Tools')
	parser.add_argument('--address', required=True, help='TransmissionBT address')
	parser.add_argument('--port', required=False, default=9091, help='TransmissionBT port')
	args = parser.parse_args()

	tool = TransmissionTools.build_using_address(args.address, args.port)
	tool.uncheck_sample()
	tool.uncheck_advertisement()
