import base64
import io

import aiohttp

from app.exceptions.application import AppException


class ImageComparator:

    def __init__(self, deepai_api_url, deepai_api_key, logger):
        self._deepai_api_url = deepai_api_url
        self._deepai_api_key = deepai_api_key
        self._logger = logger
        self._first_image_stream = None
        self._second_image_stream = None

    async def get_distance(self, first_image, second_image):
        try:
            self._first_image_stream = self._get_stream(first_image)
            self._second_image_stream = self._get_stream(second_image)
            return await self._get_images_similarity(self._first_image_stream, self._second_image_stream)
        finally:
            if self._first_image_stream is not None:
                self._first_image_stream.close()
                self._first_image_stream = None
            if self._second_image_stream is not None:
                self._second_image_stream.close()
                self._second_image_stream = None

    def _get_stream(self, content):
        actual_content = content.split('base64,')[-1]
        stream = io.BytesIO(base64.b64decode(actual_content))
        return stream

    async def _get_images_similarity(self, first_image_stream, second_image_stream):
        response = await self._get_response_from_service(first_image_stream, second_image_stream)
        self._logger.info(f'Response from Deep AI: {response}')
        if 'output' not in response:
            raise AppException('Deep AI service is not available, try later (\'output\' field is missing).')
        if 'distance' not in response['output']:
            raise AppException('Deep AI service is not available, try later (\'distance\' field is missing).')
        return response['output']['distance']

    async def _get_response_from_service(self, first_image_stream, second_image_stream):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self._deepai_api_url,
                    data={
                        'image1': first_image_stream,
                        'image2': second_image_stream,
                    },
                    headers={
                        'api-key': self._deepai_api_key
                    }
            ) as resp:
                return await resp.json()
