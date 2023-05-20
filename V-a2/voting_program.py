from voting_lib import Voting

if __name__ == '__main__':
    voting = Voting()
    voting.create_txt_file_if_not_exit()
    voting.loading_all_data_of_user()
    voting.loading_all_data_of_students()
    voting.main_option()