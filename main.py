from download_data import download_data
from match_voters import match_voters_with_voter_id

if __name__ == '__main__':
    for i in range(1, 5):
        download_data(i)
    
    match_voters_with_voter_id()
    print("Done matching. Saved results to matched_data folder.")
