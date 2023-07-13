#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket # for the video stream
from .ImageList import ImageList
from .Viewer import Viewer
from typing import Tuple

from javascript import require
mineflayerViewer = require('prismarine-viewer').headless

class MineflayerViewer(threading.Thread,Viewer):
	def __init__(self, port: int, size: Tuple[int,int] = (512, 512), printer = lambda msg: print(msg)):
		threading.Thread.__init__(self)
		Viewer.__init__(self, size, printer)
		
		self._port = port
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._socket.bind(("127.0.0.1", port))
		self._socket.listen(10)

		self._images = ImageList()

	def setup(self, bot):
		self._bot = bot
		self._client_socket = mineflayerViewer(self._bot, { 'output': '127.0.0.1:' + str(self._port), 'frames': -1, 'width': self._size[0], 'height': self._size[1], 'firstPerson': True })
		self.start()

	def run(self):
		self._printer("[v] Starting video thread...")
		self._conn, _ = self._socket.accept()

		self._close = False
		while not self._close: # TODO sync
			length = MineflayerViewer.recvint(self._conn)
			if length is None: break # closed connection
			stringData = MineflayerViewer.recvall(self._conn, int(length))
			self._images.append(stringData)

		self._printer("[v] Terminating video socket connection...")


	def close(self):
		self._close = True # TODO sync

		# close the mineflayerViewer socket connection
		# mineflayerViewer listens for @On('end') and closes the connection
		self._client_socket.end()
		self._client_socket.destroy()

		self._socket.shutdown(socket.SHUT_RDWR)
		self._socket.close()

	def start_recording(self) -> int:
		return self._images.start_recording()
	
	def stop_recording(self, id: int, out: str):
		try:
			self._images.stop_recording(id, out)
		except Exception as ex:
			self._printer(f"[e] {ex}")

	@staticmethod
	def recvall(sock, count):
		buf = b''
		while count:
			newbuf = sock.recv(count)
			if not newbuf: return None
			buf += newbuf
			count -= len(newbuf)
		return buf

	@staticmethod
	def recvint(sock) -> int:
		bytes_read = MineflayerViewer.recvall(sock, 4)
		if bytes_read is None: return None
		return int.from_bytes(bytes_read, byteorder='little')