/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;
I2C_HandleTypeDef hi2c3;

UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */
//static const uint16_t DEF_SLAVE_ADDR = 0X51<<1; //7 bit addr, shift by 1 bit

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_I2C3_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);
//void HAL_SMBUS_MasterRxCpltCallback (SMBUS_HandleTypeDef * hsmbus1);
int error;
uint16_t DEF_SLAVE_ADDR/* = 0X51<<1*/;
uint8_t reply[2];
uint16_t command_addr;
uint8_t command_arg[2]; //trying commands of 1 byte long for now
uint8_t command[6];
uint8_t length;
uint8_t ok_1;
uint8_t ok;
uint8_t ok_2;
uint8_t ok_3;
uint8_t arg_ok;
uint8_t addr_ok;
uint8_t read_ok;
uint8_t send_uart_ok;
uint8_t uart_command_ok;
uint8_t i2c_command_ok;
uint16_t PAGE_ADDR;
uint16_t OP_ADDR;
uint16_t VOUT_ADDR;
uint16_t READ_VOUT_ADDR;
uint8_t PAGE_1;
uint8_t OP_EN;
uint8_t VOUT_6_2[2];
uint8_t VOUT_9_7[2];

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */
  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */
  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_USART2_UART_Init();
  MX_I2C3_Init();
  /* USER CODE BEGIN 2 */
  //uint16_t DEF_SLAVE_ADDR = 0X51<<1;

  uint8_t reply[2];
  uint16_t command_addr;
  uint8_t command_arg[2]; //trying commands of 1 byte long for now
 // uint8_t command[5];
  uint8_t length;



  PAGE_ADDR = 0x00;
  PAGE_1 = 0x01;

  OP_ADDR = 0x01;
  OP_EN = 0x80;

  VOUT_ADDR = 0x21;
  VOUT_6_2[0] = 0x33;
  VOUT_6_2[1] = 0x06;

  READ_VOUT_ADDR = 0x8B;

  VOUT_9_7[0] = 0X07;
  VOUT_9_7[1] = 0X09;
  error = 0b00000000;
  //HAL_SMBUS_Master_Receive_IT(&hsmbus1,DEF_SLAVE_ADDR,  (uint8_t*)reply,sizeof(reply), 10);
  //HAL_UART_Receive_IT(&huart2, (uint8_t*)command, 10);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  //can we access the acknowledge bit?
  //in one write, we send 3 bytes
  //first byte is the address of the memory we want to read/write to -> command?. the following 2 bytes is the data into or out of the mem

  /*Enables Module A1 with 5.85V, reads it, sends V back to python file*/

//  ok_1 = HAL_I2C_Mem_Write(&hi2c3, DEF_SLAVE_ADDR, PAGE_ADDR, I2C_MEMADD_SIZE_8BIT, &PAGE_1, 1, 100);
//  ok_2 = HAL_I2C_Mem_Write(&hi2c3, DEF_SLAVE_ADDR, VOUT_ADDR, I2C_MEMADD_SIZE_8BIT, &VOUT_6_2, 1, 100);
//  ok_2 = HAL_I2C_Mem_Write(&hi2c3, DEF_SLAVE_ADDR, OP_ADDR, I2C_MEMADD_SIZE_8BIT, &OP_EN, 1, 100);
  //read_ok = HAL_I2C_Mem_Read(&hi2c3, DEF_SLAVE_ADDR, READ_VOUT_ADDR, I2C_MEMADD_SIZE_8BIT, &reply, 2, 15);
  //send_uart_ok = HAL_UART_Transmit_IT(&huart2, &reply, 2);


  while (1)
  {
    /* USER CODE END WHILE */
	  uart_command_ok  = HAL_UART_Receive_IT(&huart2, command, 6);
    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE2);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

/**
  * @brief I2C3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C3_Init(void)
{

  /* USER CODE BEGIN I2C3_Init 0 */

  /* USER CODE END I2C3_Init 0 */

  /* USER CODE BEGIN I2C3_Init 1 */

  /* USER CODE END I2C3_Init 1 */
  hi2c3.Instance = I2C3;
  hi2c3.Init.ClockSpeed = 100000;
  hi2c3.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c3.Init.OwnAddress1 = 0;
  hi2c3.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c3.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c3.Init.OwnAddress2 = 0;
  hi2c3.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c3.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C3_Init 2 */

  /* USER CODE END I2C3_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
	 huart2.Instance = USART2;
	  huart2.Init.BaudRate = 2400;
	  huart2.Init.WordLength = UART_WORDLENGTH_8B;
	  huart2.Init.StopBits = UART_STOPBITS_1;
	  huart2.Init.Parity = UART_PARITY_NONE;
	  huart2.Init.Mode = UART_MODE_TX_RX;
	  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
	  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
	  if (HAL_UART_Init(&huart2) != HAL_OK)
	  {
	    Error_Handler();
	  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : LD2_Pin */
  GPIO_InitStruct.Pin = LD2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LD2_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : AC_Fail_Pin OTP_Pin */
  GPIO_InitStruct.Pin = AC_Fail_Pin|OTP_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : FAN_Fail_Pin PG_Global_Pin */
  GPIO_InitStruct.Pin = FAN_Fail_Pin|PG_Global_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pin : PB1 */
  GPIO_InitStruct.Pin = GPIO_PIN_1;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */
/* Interrupt function
 * Requires: UART instance
 * If UART2 is triggered (command sent from server), nucleo transmits message to power supply*/

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	HAL_GPIO_TogglePin(LD2_GPIO_Port,LD2_Pin);
	if(huart -> Instance == USART2){
		DEF_SLAVE_ADDR = command[0]<<1;
		if(command[1] == 0){ //write
			command_arg[0] = command[4];
			command_arg[1] = command[5];
			command_addr = command[3];
			length = command[2];
			i2c_command_ok = HAL_I2C_Mem_Write(&hi2c1, DEF_SLAVE_ADDR, command_addr , I2C_MEMADD_SIZE_8BIT, command_arg, length, 10);

			//i2c_command_ok = HAL_I2C_Mem_Write(&hi2c3, DEF_SLAVE_ADDR, command[2] , I2C_MEMADD_SIZE_8BIT, command[3], command[1], 10);
		}
		else{ // command[1] == 1 read
			read_ok = HAL_I2C_Mem_Read(&hi2c1, DEF_SLAVE_ADDR, command[3] , I2C_MEMADD_SIZE_8BIT, &reply, command[2], 10);
			send_uart_ok = HAL_UART_Transmit(&huart2, &reply, command[2], 10);
		}
	}
}

/* Interrupt function
 * Requires: UART instance
 * If i2c is triggered (reply sent from power supply), nucleo transmits message to server
 */
//is there an overflow if it sends lots of commands and miss shooting
	//what happens then?
	//same time commands, which interupt
	//which is the priority - double check - can always resend command but would want to know error msg
	// run serial link as fast as we can at leat 115200 (max) go fro 2MHz, spending less time in isr and more quick to deal with other stuff - "hurry up and wait" get everything done quickly to sit in idle :)
// what happens if you receive properly formatted null response? set a flag?
// also set LED for commands sent/receive?

/*
void HAL_SMBUS_MasterRxCpltCallback (SMBUS_HandleTypeDef * hsmbus1) {
	// handles data received from Excelsys
	HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
	HAL_SMBUS_Master_Receive_IT(&hsmbus1, DEF_SLAVE_ADDR, reply,sizeof(reply), 10);
	HAL_UART_Transmit(&huart2, reply, sizeof(reply), 200); // 2 bytes long
}*/

//need to think about how to handle errors
// EXTI Line9 External Interrupt ISR Handler CallBackFun

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	// want to assign reply the same way that status word does. assign bits for
	// each error. -- how to assign bits in C?
	// B2 = OTP
	// B4 = PG
	// B1 = Fan Fail
	// B3 = AC fail
// how long do these gpio's stay on for? would we miss the error?
	error = 0b00000000;
    if(GPIO_Pin == PG_Global_Pin) // If The INT Source Is EXTI Line9 (A9 Pin)
    {
    	error = error | 0b00001000;
    	//HAL_UART_Transmit(&huart2, "Error: PG", sizeof(reply), 200); // Toggle The Output (LED) Pin
    }
    if(GPIO_Pin == FAN_Fail_Pin) // If The INT Source Is EXTI Line9 (A9 Pin)
        {
    	 error = error | 0b00000001;
    		//HAL_UART_Transmit(&huart2, "Error: FAN", sizeof(reply), 200); // Toggle The Output (LED) Pin
        }
    if(GPIO_Pin == AC_Fail_Pin) // If The INT Source Is EXTI Line9 (A9 Pin)
        {
    	 error = error | 0b00000100;
    		//HAL_UART_Transmit(&huart2, "Error: AC", sizeof(reply), 200); // Toggle The Output (LED) Pin
        }
    if(GPIO_Pin == OTP_Pin) // If The INT Source Is EXTI Line9 (A9 Pin)
        {
    	 error = error | 0b00000010;
    		//HAL_UART_Transmit(&huart2, "Error: OTP", sizeof(reply), 200); // Toggle The Output (LED) Pin
        }
    HAL_GPIO_TogglePin(LD2_GPIO_Port,LD2_Pin);
    HAL_UART_Transmit(&huart2, error, sizeof(error), 200);
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
