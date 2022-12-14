## Evaluation of Implementation Methods
	- ### Parallel method
		- The parallel method involves having both the new system and the old system running simultaneously for a period of time.
		- Pros:
			- Allows the users of the original system to learn the new system slowly, still having access to the old system.
			- Provides a back system to fall back on if the new system goes down or fails.
			- Allows major problems and bugs to be fixed through comparison to the old system
		- Cons:
			- Can be very expensive to keep both systems running at the same time.
			- The difference bewteen the systems and the way they accept data can cause data loss.
			- Can take a long time to completely switch over due to the option to use old system still being available
	- ### Phased Method
		- The phased method involves gradually in introducing the new system in phases. This can happen over a couple weeks or a couple months, the time period varies widely. At each phase one part of the old system will be removed and replaced by the newer systems part. Will often be used for the implementation of larger systems as introducing the whole system at once is often not possible.
		- Pros:
			- Allows for thorough testing of each new phase of the system before the next system, allow for the ironing out of bugs and problems
		- Cons:
			- Due to the long timeframe of implementation, this method can be very expensive.
			- Easy for data to be mixed up and/or lost due to the mixed and matched parts of the systems.
			- Users of the system can be less productive due to having to adapt to using various parts of two systems at the same time, thus decreasing their revenue producing ability and increasing cost.
	- ### Pilot Method
		- The pilot method involves giving a small group of users from a large user base various new modules from the new system to test both their functionality as well as the groups receptiveness to the new system as an indication of how the user base as a whole will adapt to the implementation of new modules. Often used to test how the system will be taken and used by the user base without the risk of a business wide failure.
		- Pros:
			- Allows each new module to be stress tested and picked apart too find inconsistencies and bugs that need to be fixed before a wide scale deployment is feasible.
		- Cons:
			- Needs a very large user base in order to be successful. Pilot group needs to be big enough to have best chance of catching errors and group receptiveness, while also being a small enough portion of the user base as a whole in order to prevent the user base refusing to adapt.
			- Data loss can also be an issue as the new modules may interpret data differently.
	- ### Direct cut-over
		- The direct cut-over method involves the complete abandoning of the old system and the deployment of the new system with almost no overlap. For example, a business may close their business on a Friday and over the weekend shutdown the old system and bring the new system online for a Monday morning opening.
		- Pros:
			- This method can be done in a very short time period and there is no need for overlapping uptime of the two systems.
			- As a result of the short time period, this method is also the cheapest available to those looking to implement new software.
		- Cons:
			- There is no backup system running in case the new system fails.
			- Doesn't allow for time for user to learn the ins and outs of the system.
			- Can cause employee productivity decreases due to adjustment period