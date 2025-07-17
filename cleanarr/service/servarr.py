from cleanarr.model.release import Release


class ServarrApi:
    async def get_all_downloads(self) -> list[Release]:
        pass

    async def ban_download(self, id: int):
        pass
