<?php

    require_once 'classSquare.php';
    require_once 'classTriangle.php';
    require_once 'classCircle.php';

    function generateSquare($min, $max)
    {
        //Функция для генерации квадрата
        //со случайными значениями
        $a = rand($min, $max);
        $b = rand($min, $max);
        $obj = new classSquare($a, $b);
        return $obj;
    }

    function generateCircle($min, $max)
    {
        //Функция для генерации круга
        //со случайными значениями
        $r = rand($min, $max);
        $obj = new classCircle($r);
        return $obj;
    }

    function generateTriangle($min, $max)
    {
        //Функция для генерации треугольника
        //со случайными значениями
        $a = rand($min, $max);
        $b = rand($min, $max);
        $c = rand(abs($a - $b), ($a + $b - 1));
        $obj = new classTriangle($a, $b, $c);
        return $obj;
    }

    function generateObject(
        $minCountObj,
        $maxCountObj,
        $min,
        $max
    ) {
        //Функция для генерации массива объектов
        $countObject = rand($minCountObj, $maxCountObj);

        while ($countObject >= 1) {
            $figure = rand(1, 3);

            switch ($figure) {
              case '1':
                $arrFigure[] = generateSquare($min, $max);
                break;

              case '2':
                $arrFigure[] = generateCircle($min, $max);
                break;

              case '3':
                $arrFigure[] = generateTriangle($min, $max);
                break;
            }

            $countObject--;
        }
        return $arrFigure;
    }
