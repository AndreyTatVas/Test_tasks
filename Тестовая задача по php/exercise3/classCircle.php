<?php

    require_once 'classFigure.php';

    class classCircle extends classFigure
    {
        //Класс для кругов
        public $r;

        public function __construct($r)
        {
            $this->name = 'Круг';
            $this->r = $r;
            $this->area = $this->r * $this->r * 3.14;
        }
    }
