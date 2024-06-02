import aio_pika
import asyncio
from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup():
    asyncio.create_task(consume_net_fee())

async def consume_net_fee():
    retry_attempts = 5
    retry_delay = 5  # seconds

    for attempt in range(retry_attempts):
        try:
            logger.info(f"Connecting to RabbitMQ, attempt {attempt + 1} of {retry_attempts}...")
            connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
            async with connection:
                logger.info("Connected to RabbitMQ.")
                channel = await connection.channel()
                queue = await channel.declare_queue("net_fee", auto_delete=False)

                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            net_fee_data = message.body.decode()
                            logger.info(f"Received net fee data: {net_fee_data}")
                            print(f"Received net fee data: {net_fee_data}")
                            # Process the net fee data as needed
            break
        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}")
            if attempt + 1 < retry_attempts:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("Max retry attempts reached. Could not connect to RabbitMQ.")
                raise

@app.get("/")
async def read_root():
    return {"message": "Payments service is running!"}
