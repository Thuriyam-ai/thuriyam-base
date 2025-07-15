import requests
from typing import Dict, List, Tuple
import requests.exceptions
from urllib.parse import urlencode
from core.settings import config as settings

from jobnotification.config.jobsegmentconfig import JobSegmentConfig


class JobsMSAdapter:
    service_url = settings.WI_JOBS_MS["url"]
    timeout = settings.WI_JOBS_MS["timeout"]

    @classmethod
    def get_jobs_for_notif(
        cls,
        candidate_id: int,
        segment: JobSegmentConfig,
        scan_limit: int = 100,
    ) -> Tuple[List[int], Dict]:
        """
        Returns candidate_metadata and a list of job-ids eligible for notification after performing the following
        exclusions:
            - candidate already called jobs
            - candidate failed jobs
            - non-serious jobs

        The count of jobs in the list can vary for 0 -> scan_limit since the count cannot is not guarenteed
        due to above exclusions
        """
        job_ids = []
        candidate_metadata = dict()

        try:
            _headers = {"Content-Type": "application/json"}
            _headers.update(settings.WORKINDIA_SHARED_REQUEST_HEADERS)

            _query_params = {
                "cid": candidate_id,
                "segment": segment,
                "limit": scan_limit,
            }

            _resp = requests.get(
                url=f"{cls.service_url}/internal/notif-jobs/?{urlencode(_query_params)}",
                headers=_headers,
                timeout=cls.timeout,
            )

            if _resp.status_code != 200:
                raise requests.exceptions.RequestException(
                    f"Request failure | status code: {_resp.status_code} | response: {_resp.text}"
                )
            _resp_data = _resp.json()
            job_ids = _resp_data["job_ids"]
            candidate_metadata = _resp_data["candidate_metadata"]
        except Exception as e:
            print(
                f"Error: {type(e).__name__} | cid: {candidate_id} | segment: {segment}"
            )
            raise

        return job_ids, candidate_metadata

    @classmethod
    def get_similar_jobs_for_notif(
        cls, candidate_id: int
    ) -> Tuple[List[int], Dict]:
        """
        Returns a list of similar job-ids eligible for notification after performing the following
        exclusions:
            - candidate already called jobs
            - candidate failed jobs
        """
        job_ids = []

        try:
            _headers = {"Content-Type": "application/json"}
            _headers.update(settings.WORKINDIA_SHARED_REQUEST_HEADERS)

            _query_params = {"cid": candidate_id}

            _resp = requests.get(
                url=f"{cls.service_url}/internal/similar-notif-jobs/v2/?{urlencode(_query_params)}",
                headers=_headers,
                timeout=cls.timeout,
            )

            if _resp.status_code != 200:
                raise requests.exceptions.RequestException(
                    f"Request failure | status code: {_resp.status_code} | response: {_resp.text}"
                )
            _resp_data = _resp.json()
            job_ids = _resp_data["job_ids"]

        except Exception as e:
            print(f"Error: {type(e).__name__} | cid: {candidate_id}")
            raise

        return job_ids
