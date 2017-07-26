## Fast and elegant switch/case-like dispatch

Originally published: 2011-09-02 01:17:52
Last updated: 2011-09-02 01:49:40
Author: Jan Kaliszewski

My approach to that common issue focuses on **efficiency** and **elegant, declarative style** of definition. That's why:\n\n* The way switches work is based on unwrapped defaultdict/list lookup.\n* The way you define switches is based on classes and easy-to-use decorators (note that you can use subclassing in a flexible way -- without any negative impact on efficiency!).\n* Its use cases focus on a-lot-of-keys situations and it does not cover the *fall-through* feature (though you can reach its semantics if you really need that -- by calling class methods...).