<?php

    require_once 'classFigure.php';

    class classSquare extends classFigure
    {
        //Класс для прямоугольников
        public $a, $b;

        public function __construct($a, $b)
        {
            $this->name = 'Прямоугольник';
            $this->a = $a;
            $this->b = $b;
            $this->area = $this->a * $this->b;
        }
    }
