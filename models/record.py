from datetime import datetime


class Record:
    def __init__(self, form, file_location):
        self.created_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.student_name = form.get('student_name', None)
        self.teacher_helping = form.get('teacher_helping')
        self.gender = form.get('gender')
        self.kindergarten_group = form.get('kindergarten_group')
        self.center_name = form.get('center_name')
        self.birthday = form.get('birthday')
        self.prompt = form.get('prompt')
        self.level_of_study = form.get('level_of_study')
        self.mother_tongue = form.get('mother_tongue')
        self.recorder_1 = form.get('recorder_1')
        self.recorder_2 = form.get('recorder_2')
        self.wav_file_location = file_location
        self.grading_algo = form.get('grading_algo', 'wer2')
        self.good = form.get('good')
        self.fluency_score = form.get('fluency_score')
        self.noise_level = form.get('noise_level')
        self.accuracy_score = form.get('accuracy_score')
        self.remarks = form.get('remarks', '')

    def dump(self):
        return [[
            self.created_at, self.student_name, self.teacher_helping, self.gender, self.kindergarten_group, self.center_name, self.birthday, self.level_of_study, self.mother_tongue, self.recorder_1, self.recorder_2, self.prompt, self.wav_file_location, self.good, self.fluency_score, self.noise_level, self.accuracy_score, 
            self.grading_algo, self.grade, self.accuracy, self.loss, self.remarks
        ]]

    def _evaluate(self, result):
        '''
        {
        "result": "success",
        "scores": {
            "WER": 0.143,
            "acc": 0.857,
            "loss": 0.143,
            "numCor": 6,
            "numCount": 7,
            "numDel": 0,
            "numIns": 0,
            "numSub": 1
            }
        }
        '''
        self.grade = result["WER"]
        self.accuracy = result["acc"]
        self.loss = result["loss"]
