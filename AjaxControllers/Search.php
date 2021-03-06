<?php

class SearchController extends AjaxController {
	public $template = "Search";
	public function process($get,$post) {
		// Select all of the courses that this user is already added
		$query = new Query('action');
		$result = $query->select('*', array(array('session_id', '=', $_COOKIE['sessionId'])));
		$idsAlreadyAdded = array();
		foreach($result as $action){
			array_push($idsAlreadyAdded, $action->get('course_id'));
		}
		// Select all the courses where the query string is a sub-string of the name or id
		$query = new Query('courses');
		$result = $query->select('*', array(array('name', 'LIKE', '%'.$post['q'].'%'), 'OR', array('number', 'LIKE', '%'.$post['q'].'%')), array('number', 'ASC'), 100);
		$courses = array();
		foreach($result as $course){
			if(!in_array($course->get('id'), $idsAlreadyAdded)){ // Check that this course has not been added by the user yet
				array_push($courses, array('id' => $course->get('id'),
											  'name' => ucwords(strtolower($course->get('name'))),
											  'department_id' => $course->get('department_id'),
											  'number' => $course->get('number'),
											  'description' => ((strlen($course->get('description'))==0)?'No description':$course->get('description'))));
			}
		}
		$this->pageData['courseResults'] = $courses;
		return true;
	}
}

?>