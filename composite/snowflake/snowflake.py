# Copyright (c) 2012 Alexander V. Nikolaev <avn@daemon.hole.ru>
# This code derived from idworker.py from pysnowlake by Eran Sandler
# 
# Copyright (c) 2011 Eran Sandler (eran@sandler.co.il)
# http://eran.sandler.co.il
# http://forecastcloudy.net
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import time
import logging
try:
    import threading
except ImportError:
    import dummy_threading as threading

class Snowflake(object):
    def __init__(self, data_center_id, worker_id):
        self.worker_id = worker_id
        self.data_center_id = data_center_id

        self.logger = logging.getLogger("snowflake")

        # stats
        self.ids_generated = 0

        # Tue, 21 Mar 2006 20:50:14.000 GMT
        self.twepoch = 1142974214000L
        
        self.sequence = 0L
        self.worker_id_bits = 5L
        self.data_center_id_bits = 5L
        self.max_worker_id = -1L ^ (-1L << self.worker_id_bits)
        self.max_data_center_id = -1L ^ (-1L << self.data_center_id_bits)
        self.sequence_bits = 12L

        self.worker_id_shift = self.sequence_bits
        self.data_center_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = self.sequence_bits + self.worker_id_bits + self.data_center_id_bits
        self.sequence_mask = -1L ^ (-1L << self.sequence_bits)

        self.last_timestamp = -1L

        # Sanity check for worker_id
        if self.worker_id > self.max_worker_id or self.worker_id < 0:
            raise InputError("worker_id", "worker id can't be greater than %i or less than 0" % self.max_worker_id)

        if self.data_center_id > self.max_data_center_id or self.data_center_id < 0:
            raise InputError("data_center_id", "data center id can't be greater than %i or less than 0" % self.max_data_center_id)

        self.logger.info("worker starting. timestamp left shift %d, data center id bits %d, worker id bits %d, sequence bits %d, worker id %d" % (self.timestamp_left_shift, self.data_center_id_bits, self.worker_id_bits, self.sequence_bits, self.worker_id))

    def _time_gen(self):
        return long(int(time.time() * 1000))
     
    def _till_next_millis(self, last_timestamp):
        timestamp = self._time_gen()
        while last_timestamp <= timestamp:
            timestamp = self._time_gen()

        return timestamp
   
    def _next_id(self):
        timestamp = self._time_gen()
        
        if self.last_timestamp > timestamp:
            self.logger.warning("clock is moving backwards. Rejecting request until %i" % self.last_timestamp)
            raise InvalidSystemClock("Clock moved backwards. Refusing to generate id for %i milliseocnds" % self.last_timestamp)

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._till_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - self.twepoch) << self.timestamp_left_shift) | (self.data_center_id << self.data_center_id_shift) | (self.worker_id << self.worker_id_shift) | self.sequence
        self.ids_generated += 1
        return new_id

    def _valid_user_agent(self, user_agent):
        return self.user_agent_parser.search(user_agent) is not None

    def get_timestamp(self):
        return self._time_gen()

    def get_id(self):
        new_id = self._next_id()
        self.logger.debug("id: %i  worker_id: %i  data_center_id: %i" % 
            (new_id, self.worker_id, self.data_center_id))
        return new_id

class ThreadSafeSnowflake(Snowflake):
    def __init__(self, datacenter_id, worker_id):
        super(ThreadSafeSnowflake, self).__init__(datacenter_id, worker_id)
        self.condition = threading.Condition(threading.Lock())

    def get_id(self):
        self.condition.acquire()
        try:
            return super(ThreadSafeSnowflake, self).get_id()
        finally:
            self.condition.release()

if __name__ == "__main__":
    # little test
    import base64
    from pickle import encode_long
    s = ThreadSafeSnowflake(0, 2)
    for x in range(1, 20):
        y = s.get_id()
        print y
        b = encode_long(y)
        print base64.b32encode(b)
        print base64.urlsafe_b64encode(b), len(base64.urlsafe_b64encode(b))
