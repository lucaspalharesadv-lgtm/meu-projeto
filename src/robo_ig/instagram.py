import os
import time

import requests

from .config import Config


class InstagramError(RuntimeError):
    pass


class InstagramClient:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.base = f"https://graph.facebook.com/{cfg.graph_version}"

    def _call(self, method: str, path: str, **params):
        params["access_token"] = self.cfg.ig_token
        r = requests.request(method, f"{self.base}/{path}", params=params if method == "GET" else None,
                             data=params if method == "POST" else None, timeout=60)
        body = r.json()
        if r.status_code >= 400 or "error" in body:
            raise InstagramError(str(body.get("error", body)))
        return body

    def public_url(self, local_path: str) -> str:
        rel = os.path.relpath(local_path, self.cfg.media_dir).replace(os.sep, "/")
        return f"{self.cfg.public_base_url}/{rel}"

    def _wait_ready(self, container_id: str, tries: int = 30) -> None:
        for _ in range(tries):
            status = self._call("GET", container_id, fields="status_code").get("status_code")
            if status == "FINISHED":
                return
            if status in ("ERROR", "EXPIRED"):
                raise InstagramError(f"container {container_id}: {status}")
            time.sleep(4)
        raise InstagramError(f"container {container_id}: timeout")

    def publish_images(self, image_paths: list[str], caption: str, alt_text: str = "") -> str:
        uid = self.cfg.ig_user_id
        urls = [self.public_url(p) for p in image_paths]
        if len(urls) == 1:
            container = self._call("POST", f"{uid}/media", image_url=urls[0], caption=caption, alt_text=alt_text)["id"]
        else:
            children = []
            for url in urls:
                cid = self._call("POST", f"{uid}/media", image_url=url, is_carousel_item="true")["id"]
                self._wait_ready(cid)
                children.append(cid)
            container = self._call("POST", f"{uid}/media", media_type="CAROUSEL",
                                   children=",".join(children), caption=caption)["id"]
        self._wait_ready(container)
        return self._call("POST", f"{uid}/media_publish", creation_id=container)["id"]

    def publish_reel(self, video_path: str, caption: str) -> str:
        uid = self.cfg.ig_user_id
        container = self._call("POST", f"{uid}/media", media_type="REELS", video_url=self.public_url(video_path),
                               caption=caption, share_to_feed="true")["id"]
        self._wait_ready(container, tries=90)
        return self._call("POST", f"{uid}/media_publish", creation_id=container)["id"]

    def insights(self, media_id: str) -> dict:
        data = self._call("GET", f"{media_id}/insights", metric="reach,likes,comments,saved,shares")["data"]
        return {m["name"]: m["values"][0]["value"] for m in data}

    def send_dm(self, recipient_id: str, text: str) -> None:
        self._call_json(f"{self.cfg.ig_user_id}/messages", {"recipient": {"id": recipient_id}, "message": {"text": text}})

    def private_reply(self, comment_id: str, text: str) -> None:
        self._call_json(f"{self.cfg.ig_user_id}/messages", {"recipient": {"comment_id": comment_id}, "message": {"text": text}})

    def _call_json(self, path: str, payload: dict):
        r = requests.post(f"{self.base}/{path}", params={"access_token": self.cfg.ig_token}, json=payload, timeout=30)
        body = r.json()
        if r.status_code >= 400 or "error" in body:
            raise InstagramError(str(body.get("error", body)))
        return body
