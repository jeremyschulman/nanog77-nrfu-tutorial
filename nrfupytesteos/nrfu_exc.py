#  Copyright 2019 Jeremy Schulman, nwkautomaniac@gmail.com
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class NrfuError(RuntimeError):
    def __init__(self, *vargs, extra=None):
        super(NrfuError, self).__init__(*vargs)
        self.extra = extra or ''


class MissingError(NrfuError):
    def __init__(self, *vargs, missing=None):
        super(MissingError, self).__init__(*vargs)
        self.missing = missing

    def __str__(self):
        emsg = super(MissingError, self).__str__()
        msg = f"MISSING data: {self.missing}"
        return '\n'.join((emsg, msg, self.extra))


class UnexpectedError(NrfuError):
    def __init__(self, *vargs, unexpected=None):
        super(UnexpectedError, self).__init__(*vargs)
        self.unexpected = unexpected

    def __str__(self):
        emsg = super(UnexpectedError, self).__str__()
        msg = f"UNEXPECTED data: {self.unexpected}"
        return '\n'.join((emsg, msg, self.extra))


class MismatchError(NrfuError):
    def __init__(self, *vargs, expected=None, actual=None):
        super(MismatchError, self).__init__(*vargs)
        self.expected = expected
        self.actual = actual

    def __str__(self):
        emsg = super(MismatchError, self).__str__()
        exp_msg = f"MISMATCH:EXPECTED data: {self.expected or 'None'}"
        act_msg = f"MISMATCH:ACTUAL data: {self.actual or 'None'}"
        return '\n'.join((emsg, exp_msg, act_msg, self.extra))
