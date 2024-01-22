from hstest import StageTest, dynamic_test, CheckResult, WrongAnswer, TestedProgram


class Test(StageTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()

        reply = program.start()

        self.check_empty_or_none_output(reply)
        self.check_number_of_notes_prompt(reply)

        reply = program.execute("2")
        self.check_empty_or_none_output(reply)
        self.check_user_prompt(reply)

        for i in range(1, 3):
            reply = program.execute(f'update {i} Updated first note!')
            self.check_empty_or_none_output(reply)
            self.check_command_response(
                reply, '[Error] There is nothing to update')
            self.check_user_prompt_after_command(reply)

            reply = program.execute(f'delete {i}')
            self.check_empty_or_none_output(reply)
            self.check_command_response(
                reply, '[Error] There is nothing to delete')
            self.check_user_prompt_after_command(reply)

        reply = program.execute('create')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Error] Missing note argument')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('del 2')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Error] Unknown command')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('list')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Info] Notepad is empty')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('create This is my first record!')
        self.check_empty_or_none_output(reply)
        self.check_command_response(
            reply, '[OK] The note was successfully created')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('update 1')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Error] Missing note argument')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('update one Updated first note!')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Error] Invalid position: one')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('update')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Error] Missing position argument')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('update 10')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Error] Missing note argument')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('update 10 Updated tenth note!')
        self.check_empty_or_none_output(reply)
        self.check_command_response(
            reply, '[Error] Position 10 is out of the boundaries [1, 2]')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('update 1 Updated first note!')
        self.check_empty_or_none_output(reply)
        self.check_command_response(
            reply, '[OK] The note at position 1 was successfully updated')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('list')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Info] 1: Updated first note!')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('create This is my second record!')
        self.check_empty_or_none_output(reply)
        self.check_command_response(
            reply, '[OK] The note was successfully created')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('delete one')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Error] Invalid position: one')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('delete')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Error] Missing position argument')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('delete 1')
        self.check_empty_or_none_output(reply)
        self.check_command_response(
            reply, '[OK] The note at position 1 was successfully deleted')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('list')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Info] 1: This is my second record!')
        self.check_user_prompt_after_command(reply)

        reply = program.execute(f'create This is my second record!')
        self.check_empty_or_none_output(reply)
        self.check_command_response(
            reply, '[OK] The note was successfully created')
        self.check_user_prompt_after_command(reply)

        reply = program.execute(f'clear')
        self.check_empty_or_none_output(reply)
        self.check_command_response(
            reply, '[OK] All notes were successfully deleted')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('list')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Info] Notepad is empty')
        self.check_user_prompt_after_command(reply)

        reply = program.execute('exit')
        self.check_empty_or_none_output(reply)
        self.check_command_response(reply, '[Info] bye!')

        return CheckResult.correct()

    @staticmethod
    def check_command_response(raw_output, message=''):
        output = raw_output.strip().lower().split("\n")[0]
        if not message and output:
            raise WrongAnswer(
                'The program should print nothing.\n'
                f'Your output: {raw_output}.'
            )
        if not output.strip().startswith(message.lower()):
            raise WrongAnswer(
                f'The program should print "{message}".\n'
                f'Your output: "{raw_output}".'
            )

    def check_user_prompt_after_command(self, raw_output):
        output = raw_output.strip().lower().split("\n")
        if len(output) < 2:
            raise WrongAnswer('The program should ask user for a command.')

        self.check_user_prompt(output[1])

    @staticmethod
    def check_number_of_notes_prompt(raw_output):
        prompt = 'Enter the maximum number of notes:'
        if not raw_output.strip().lower().startswith(prompt.lower()):
            raise WrongAnswer(
                'The program should ask user to enter the maximum number of notes\n'
                f'Your output should be equal to "{prompt}".\n'
                f'Your output: "{raw_output}".'
            )

    @staticmethod
    def check_user_prompt(raw_output):
        prompt = 'Enter a command and data:'
        if not raw_output.strip().lower().startswith(prompt.lower()) and raw_output != '':
            raise WrongAnswer(
                'The program should ask user for a command.\n'
                f'Your output should be equal to "{prompt}".\n'
                f'Your output: "{raw_output}".'
            )

    @staticmethod
    def check_empty_or_none_output(raw_output):
        if not raw_output:
            raise WrongAnswer('Your output is empty or None.')


if __name__ == '__main__':
    Test().run_tests()
