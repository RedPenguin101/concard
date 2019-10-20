# Ubiquitous Language
* Card
	* Title
	* Body
	* Parent
	* ReviewHistory: tuples of date and response
	* NextReview
	* References

* Question - Answer
	* QuestionHistory: tuples of date and success
	* NextQuiz

* Review
	* Date
	* CardReview
	* Questions

* CardReview
	* ReviewDate
	* Response
	* NextReview


# todo
* Card CRUD
	* ~~create~~ DONE
	* ~~update~~ DONE
	* ~~read~~ DONE
	* ~~delete~~ DONE
* move parent
* ~~text size validation - warning on UI if text exceeds 500char~~ DONE
* write Concard class which acts as an app, then redo app as a Json frontend to that?
* add Reviews (note: store these separately for ease of loading. Should be able to load a list of todays reviews then load those cards)
	* Review domain object
	* load (is there a separate repo class for this? or done by filters?)
	* LoadTodaysReviews command
	* SaveReviewResults command
	* save
* add questions

